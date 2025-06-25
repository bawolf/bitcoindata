"""
Simple Flask web application example for Bitcoin ATH analysis.
This demonstrates how to deploy the analyzer as a website.

To run in production, you'd want to use a proper WSGI server like Gunicorn.
"""

from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime, timedelta
import threading
import time
import os

# Import our analyzer components
from bitcoin_ath_analyzer import BitcoinATHAnalyzer
from api_integrations import BitcoinPriceAPI, DailyUpdateManager

app = Flask(__name__)

# Global variables to store analysis data
analyzer = None
price_api = None
update_manager = None
last_analysis = None
last_update = None

def initialize_app():
    """Initialize the analyzer components"""
    global analyzer, price_api, update_manager
    
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
    
    # Load initial data
    print("Loading initial Bitcoin data...")
    try:
        analyzer.download_bitcoin_data()
        analyzer.calculate_ath_distances()
        print("✅ Initial data loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load initial data: {e}")

def update_analysis():
    """Update the analysis data"""
    global last_analysis, last_update
    
    try:
        result = update_manager.run_daily_update()
        if result['success']:
            last_analysis = result
            last_update = datetime.now()
            print(f"✅ Analysis updated: {result['current_distance_from_ath']:.2f}% from ATH")
        else:
            print(f"❌ Analysis update failed: {result.get('error', 'Unknown error')}")
    except Exception as e:
        print(f"❌ Analysis update exception: {e}")

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/current-analysis')
def api_current_analysis():
    """API endpoint to get current analysis data"""
    if last_analysis is None:
        # Trigger an update if no data exists
        update_analysis()
    
    if last_analysis and last_analysis['success']:
        return jsonify({
            'success': True,
            'data': last_analysis,
            'last_updated': last_update.isoformat() if last_update else None
        })
    else:
        return jsonify({
            'success': False,
            'error': 'No analysis data available'
        }), 500

@app.route('/api/historical-data')
def api_historical_data():
    """API endpoint to get historical ATH distance data"""
    if analyzer is None or analyzer.ath_data is None:
        return jsonify({
            'success': False,
            'error': 'No historical data available'
        }), 500
    
    try:
        # Get the requested time range (default to 365 days)
        days = request.args.get('days', default=365, type=int)
        
        # Handle special cases
        if days == -1:  # All time
            recent_data = analyzer.ath_data
        else:
            recent_data = analyzer.ath_data.tail(days)
        
        chart_data = {
            'dates': [date.strftime('%Y-%m-%d') for date in recent_data.index],
            'distances': [float(x) for x in recent_data['Distance_from_ATH_Pct'].tolist()],
            'ath_values': [float(x) for x in recent_data['ATH'].tolist()],
            'high_values': [float(x) for x in recent_data['High'].tolist()]
        }
        
        return jsonify({
            'success': True,
            'data': chart_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/distribution-stats')
def api_distribution_stats():
    """API endpoint to get distribution statistics"""
    if analyzer is None or analyzer.ath_data is None:
        return jsonify({
            'success': False,
            'error': 'No data available'
        }), 500
    
    try:
        analysis = analyzer.analyze_distribution()
        
        # Convert numpy/pandas types to native Python types for JSON serialization
        json_safe_analysis = {
            'mean': float(analysis['mean']),
            'median': float(analysis['median']),
            'std': float(analysis['std']),
            'min': float(analysis['min']),
            'max': float(analysis['max']),
            'percentiles': {
                '10th': float(analysis['percentiles']['10th']),
                '25th': float(analysis['percentiles']['25th']),
                '75th': float(analysis['percentiles']['75th']),
                '90th': float(analysis['percentiles']['90th']),
                '95th': float(analysis['percentiles']['95th']),
                '99th': float(analysis['percentiles']['99th'])
            },
            'days_at_ath': int(analysis['days_at_ath']),
            'total_days': int(analysis['total_days'])
        }
        
        return jsonify({
            'success': True,
            'data': json_safe_analysis
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/distribution-histogram')
def api_distribution_histogram():
    """API endpoint to get histogram data for distribution chart"""
    if analyzer is None or analyzer.ath_data is None:
        return jsonify({
            'success': False,
            'error': 'No data available'
        }), 500
    
    try:
        distances = analyzer.ath_data['Distance_from_ATH_Pct']
        
        # Create histogram bins (50 bins from 0 to max distance)
        import numpy as np
        max_distance = distances.max()
        bins = np.linspace(0, max_distance, 51)  # 50 bins
        hist, bin_edges = np.histogram(distances, bins=bins)
        
        # Calculate bin centers for x-axis
        bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]
        
        # Get key statistics including volatility metrics
        mean_distance = distances.mean()
        median_distance = distances.median()
        std_distance = distances.std()
        coefficient_of_variation = (std_distance / mean_distance) * 100  # CV as percentage
        
        # Calculate volatility bands (mean ± 1 and 2 standard deviations)
        volatility_bands = {
            'mean_minus_2std': max(0, mean_distance - 2*std_distance),
            'mean_minus_1std': max(0, mean_distance - 1*std_distance),
            'mean_plus_1std': mean_distance + 1*std_distance,
            'mean_plus_2std': mean_distance + 2*std_distance
        }
        
        # Also calculate cumulative distribution for the cumulative chart
        sorted_distances = np.sort(distances)
        cumulative_pct = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100
        
        return jsonify({
            'success': True,
            'data': {
                'bin_centers': [float(x) for x in bin_centers],
                'counts': [int(x) for x in hist],
                'mean_distance': float(mean_distance),
                'median_distance': float(median_distance),
                'std_distance': float(std_distance),
                'coefficient_of_variation': float(coefficient_of_variation),
                'volatility_bands': {k: float(v) for k, v in volatility_bands.items()},
                'total_days': int(len(distances)),
                'cumulative_distances': [float(x) for x in sorted_distances],
                'cumulative_percentages': [float(x) for x in cumulative_pct]
            }
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/force-update', methods=['POST'])
def api_force_update():
    """API endpoint to force an update (for admin use)"""
    try:
        update_analysis()
        return jsonify({
            'success': True,
            'message': 'Update completed',
            'data': last_analysis
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

def main():
    """Main entry point for the application"""
    print("🚀 Starting Bitcoin ATH Analyzer Web App...")
    
    # Run an initial update to ensure data is available on startup
    print("Performing initial analysis update...")
    update_analysis()
    
    # Note: The background scheduler thread has been removed.
    # We will use an external scheduler (like GCP Cloud Scheduler) in production.

    # Start Flask app (for local development)
    # Production servers like Gunicorn will call the 'app' object directly.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Initialize the application for Gunicorn or other WSGI servers
initialize_app()

if __name__ == '__main__':
    main() 