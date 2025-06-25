"""
A one-off script to clear the Bitcoin data cache from Google Cloud Storage.
Run this if your cache file contains corrupted or bad data (e.g., future dates).
"""
import os
from bitcoin_ath_analyzer import BitcoinATHAnalyzer

def clear_the_cache():
    """
    Initializes the analyzer and clears the data cache on Google Cloud Storage.
    """
    # Ensure environment variables are loaded, especially GCS_BUCKET_NAME
    gcs_bucket_name = os.environ.get('GCS_BUCKET_NAME')
    
    if not gcs_bucket_name:
        print("❌ ERROR: GCS_BUCKET_NAME environment variable is not set.")
        print("Please configure it in your .envrc file and run 'direnv allow'.")
        return
        
    print(f"Targeting GCS bucket: {gcs_bucket_name}")
    
    # Initialize the analyzer to connect to GCS
    # We don't need to worry about the yfinance cache fix here, as we aren't fetching data.
    analyzer = BitcoinATHAnalyzer(gcs_bucket_name=gcs_bucket_name)
    
    print("Attempting to clear the cache...")
    try:
        analyzer.clear_cache()
        print("✅ Cache cleared successfully from GCS.")
    except Exception as e:
        print(f"❌ An error occurred while clearing the cache: {e}")

if __name__ == "__main__":
    clear_the_cache() 