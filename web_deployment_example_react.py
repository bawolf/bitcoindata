"""
Flask web application that serves a React frontend in production
and provides API endpoints for Bitcoin ATH analysis.

Development: Run Vite dev server separately for React frontend
Production: Serve built React files from Flask
"""

from flask import Flask, render_template, jsonify, request, current_app, send_from_directory
import json
from datetime import datetime, timedelta
import threading
import time
import os
import numpy as np

# Import our analyzer components
from bitcoin_ath_analyzer import BitcoinATHAnalyzer
from api_integrations import BitcoinPriceAPI, DailyUpdateManager

def create_app():
    """
    Creates and configures the Flask application with React frontend support.
    """
    app = Flask(__name__, static_folder='static/dist', static_url_path='')

    # --- Component Initialization ---
    gcs_bucket_name = os.environ.get('GCS_BUCKET_NAME')
    
    if gcs_bucket_name:
        print(f"Initializing analyzer with GCS bucket: {gcs_bucket_name}")
        analyzer = BitcoinATHAnalyzer(gcs_bucket_name=gcs_bucket_name)
    else:
        print("GCS_BUCKET_NAME not set. Initializing analyzer with local file cache.")
        analyzer = BitcoinATHAnalyzer()
        
    price_api = BitcoinPriceAPI()
    update_manager = DailyUpdateManager(analyzer, price_api)

    # --- Application Startup Logic ---
    print("Loading initial Bitcoin data...")
    try:
        analyzer.download_bitcoin_data()
        analyzer.calculate_ath_distances()
        print("✅ Initial data loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load initial data: {e}")
    
    # Store components on app context
    with app.app_context():
        current_app.analyzer = analyzer
        current_app.price_api = price_api
        current_app.update_manager = update_manager
        current_app.last_analysis = None
        current_app.last_update = None
    
    # --- Register Routes ---
    register_routes(app)

    # --- Start background job ---
    update_thread = threading.Thread(target=run_scheduled_update, args=(app,), daemon=True)
    update_thread.start()
    
    return app

def register_routes(app):
    """Register Flask routes with React frontend support."""

    @app.route('/')
    def index():
        """Serve the React app."""
        # In production, serve the built React app
        if os.path.exists(os.path.join(app.static_folder, 'index.html')):
            return send_from_directory(app.static_folder, 'index.html')
        else:
            # Fallback for development - you'd run Vite separately
            return '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Bitcoin HODL Dashboard</title>
            </head>
            <body>
                <h1>Development Mode</h1>
                <p>Please run the Vite dev server: <code>npm run dev</code></p>
                <p>Or build the React app: <code>npm run build</code></p>
            </body>
            </html>
            '''

    @app.route('/<path:path>')
    def catch_all(path):
        """Catch all routes for React Router (SPA routing)."""
        # Serve static files normally
        if '.' in path:
            return send_from_directory(app.static_folder, path)
        # For all other routes, serve the React app
        return index()

    # --- API Routes (unchanged) ---
    @app.route('/api/current-analysis')
    def api_current_analysis():
        """API endpoint for the latest ATH analysis."""
        if current_app.last_update and datetime.now() - current_app.last_update < timedelta(seconds=30):
            if current_app.last_analysis:
                return jsonify({
                    'success': True,
                    'data': current_app.last_analysis,
                    'last_updated': current_app.last_update.isoformat()
                })

        try:
            analysis_result = current_app.update_manager.run_daily_update()
            if analysis_result.get('success'):
                current_app.last_analysis = analysis_result
                current_app.last_update = datetime.now()
                return jsonify({
                    'success': True,
                    'data': analysis_result,
                    'last_updated': current_app.last_update.isoformat()
                })
            else:
                return jsonify(analysis_result), 500
        except Exception as e:
            app.logger.error(f"Error in /api/current-analysis: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/historical-data')
    def api_historical_data():
        """API endpoint to get historical ATH distance data"""
        analyzer = current_app.analyzer
        if analyzer is None or analyzer.ath_data is None:
            return jsonify({
                'success': False,
                'error': 'No historical data available'
            }), 500
        
        try:
            days = request.args.get('days', default=365, type=int)
            recent_data = analyzer.ath_data if days == -1 else analyzer.ath_data.tail(days)
            
            chart_data = {
                'dates': [date.strftime('%Y-%m-%d') for date in recent_data.index],
                'distances': [float(x) for x in recent_data['Distance_from_ATH_Pct'].tolist()],
                'ath_values': [float(x) for x in recent_data['ATH'].tolist()],
                'high_values': [float(x) for x in recent_data['High'].tolist()]
            }
            return jsonify({'success': True, 'data': chart_data})
        except Exception as e:
            app.logger.error(f"Error in /api/historical-data: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/distribution-histogram')
    def api_distribution_histogram():
        """API endpoint to get histogram data for distribution chart"""
        analyzer = current_app.analyzer
        if analyzer is None or analyzer.ath_data is None or analyzer.ath_data.empty:
            return jsonify({'success': False, 'error': 'No analysis data available to generate histogram.'}), 500
        
        try:
            distances = analyzer.ath_data['Distance_from_ATH_Pct']
            analysis = analyzer.analyze_distribution()

            # Create histogram bins
            max_distance = distances.max()
            bins = np.linspace(0, max_distance, 51)
            hist, bin_edges = np.histogram(distances, bins=bins)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            # Calculate cumulative distribution
            sorted_distances = np.sort(distances)
            cumulative_pct = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100

            # Calculate volatility metrics
            mean_distance = analysis['mean']
            std_distance = analysis['std']
            coefficient_of_variation = (std_distance / mean_distance) * 100 if mean_distance > 0 else 0
            volatility_bands = {
                'mean_minus_2std': max(0, mean_distance - 2*std_distance),
                'mean_minus_1std': max(0, mean_distance - 1*std_distance),
                'mean_plus_1std': mean_distance + 1*std_distance,
                'mean_plus_2std': mean_distance + 2*std_distance
            }

            return jsonify({
                'success': True,
                'data': {
                    'bin_centers': [float(x) for x in bin_centers],
                    'counts': [int(x) for x in hist],
                    'mean_distance': float(analysis['mean']),
                    'median_distance': float(analysis['median']),
                    'std_distance': float(analysis['std']),
                    'coefficient_of_variation': float(coefficient_of_variation),
                    'volatility_bands': {k: float(v) for k, v in volatility_bands.items()},
                    'cumulative_distances': [float(x) for x in sorted_distances],
                    'cumulative_percentages': [float(x) for x in cumulative_pct]
                }
            })
        except Exception as e:
            app.logger.error(f"Error in /api/distribution-histogram: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500

    @app.route('/api/hardest-days')
    def api_hardest_days():
        """API endpoint to get the hardest days to HODL"""
        analyzer = current_app.analyzer
        if analyzer is None or analyzer.ath_data is None or analyzer.ath_data.empty:
            return jsonify({'success': False, 'error': 'No analysis data available.'}), 500
        
        try:
            # Get top 5 hardest days
            hardest_days = analyzer.ath_data.nlargest(5, 'Distance_from_ATH_Pct')
            
            hardest_data = []
            for date, row in hardest_days.iterrows():
                hardest_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'distance_pct': float(row['Distance_from_ATH_Pct']),
                    'price': float(row['High']),
                    'ath_at_time': float(row['ATH']),
                    'dollar_loss': float(row['ATH'] - row['High'])
                })
            
            # Count easy days
            easy_days = analyzer.ath_data[analyzer.ath_data['Distance_from_ATH_Pct'] == 0.0]
            easy_days_count = len(easy_days)
            total_days = len(analyzer.ath_data)
            easy_days_pct = (easy_days_count / total_days) * 100
            
            # Get recent easy days
            recent_easy_days = easy_days.tail(5)
            easy_days_data = []
            for date, row in recent_easy_days.iterrows():
                easy_days_data.append({
                    'date': date.strftime('%Y-%m-%d'),
                    'price': float(row['High'])
                })
            
            return jsonify({
                'success': True,
                'data': {
                    'hardest_days': hardest_data,
                    'easy_days_count': easy_days_count,
                    'easy_days_percentage': float(easy_days_pct),
                    'total_days': total_days,
                    'recent_easy_days': easy_days_data
                }
            })
        except Exception as e:
            app.logger.error(f"Error in /api/hardest-days: {e}", exc_info=True)
            return jsonify({'success': False, 'error': str(e)}), 500

def run_scheduled_update(app):
    """Background thread for scheduled updates."""
    with app.app_context():
        while True:
            time.sleep(900)  # 15 minutes
            
            print("🕒 Kicking off scheduled background update...")
            try:
                analysis_result = current_app.update_manager.run_daily_update()
                if analysis_result.get('success'):
                    current_app.last_analysis = analysis_result
                    current_app.last_update = datetime.now()
                    print("✅ Background update successful.")
                else:
                    print(f"❌ Background update failed: {analysis_result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"❌ Exception in background update thread: {e}")

# Create the app instance
app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 