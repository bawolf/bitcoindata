"""
Simple Flask web application example for Bitcoin ATH analysis.
This demonstrates how to deploy the analyzer as a website.

To run in production, you'd want to use a proper WSGI server like Gunicorn.
"""

from flask import Flask, render_template, jsonify, request, current_app
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
    Creates and configures the Flask application using the factory pattern.
    This makes the application structure more robust and avoids global variables.
    """
    app = Flask(__name__)

    # --- Component Initialization ---
    # Get GCS bucket name from environment variable for cloud deployments
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
    # This runs once when the application starts.
    # It pre-loads the historical data and performs the initial analysis.
    print("Loading initial Bitcoin data...")
    try:
        analyzer.download_bitcoin_data()
        analyzer.calculate_ath_distances()  # THIS IS THE CRITICAL FIX
        print("✅ Initial data loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load initial data: {e}")
    
    # Store the initialized components and state directly on the app object.
    # This is a cleaner way to manage state than using global variables.
    with app.app_context():
        current_app.analyzer = analyzer
        current_app.price_api = price_api
        current_app.update_manager = update_manager
        current_app.last_analysis = None
        current_app.last_update = None
    
    # --- Register Routes ---
    register_routes(app)

    # --- Start background job ---
    # We start a background thread to perform a scheduled update.
    update_thread = threading.Thread(target=run_scheduled_update, args=(app,), daemon=True)
    update_thread.start()
    
    return app

def register_routes(app):
    """Register the Flask routes with the application instance."""

    @app.route('/')
    def index():
        return render_template('dashboard.html')

    @app.route('/api/current-analysis')
    def api_current_analysis():
        """
        API endpoint for the latest ATH analysis.
        Uses a simple time-based cache to avoid re-calculating on every request.
        """
        # Use a simple time-based cache to avoid hitting the update logic on every single request.
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
            
            # Perform a full analysis to get all the required stats
            analysis = analyzer.analyze_distribution()

            # Create histogram bins
            max_distance = distances.max()
            bins = np.linspace(0, max_distance, 51)
            hist, bin_edges = np.histogram(distances, bins=bins)
            bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2

            # Also calculate cumulative distribution for the cumulative chart
            sorted_distances = np.sort(distances)
            cumulative_pct = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100

            # Calculate volatility metrics required by the frontend
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


def run_scheduled_update(app):
    """
    Background thread that runs the update manager every 15 minutes.
    This ensures the main analysis data stays fresh.
    """
    with app.app_context():
        while True:
            # Wait for 15 minutes before the next run
            time.sleep(900)
            
            print("🕒 Kicking off scheduled background update...")
            try:
                # The result is stored in the app context for other requests to use.
                analysis_result = current_app.update_manager.run_daily_update()
                if analysis_result.get('success'):
                    current_app.last_analysis = analysis_result
                    current_app.last_update = datetime.now()
                    print("✅ Background update successful.")
                else:
                    print(f"❌ Background update failed: {analysis_result.get('error', 'Unknown error')}")
            except Exception as e:
                print(f"❌ Exception in background update thread: {e}")

# Create the app instance for Gunicorn to discover.
app = create_app()

if __name__ == '__main__':
    # This block is for local development.
    # It uses Flask's built-in server with debugging and auto-reloading.
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080))) 