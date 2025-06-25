import os
from bitcoin_ath_analyzer import BitcoinATHAnalyzer

def main():
    """
    This script is designed to be run as a scheduled job (e.g., on Cloud Run Jobs).
    It triggers the daily update of the Bitcoin historical data cache stored in GCS.
    
    The GCS_BUCKET_NAME environment variable must be set for this script to work.
    """
    print("🚀 Starting scheduled daily data update job...")

    gcs_bucket_name = os.environ.get('GCS_BUCKET_NAME')
    if not gcs_bucket_name:
        print("❌ FATAL: GCS_BUCKET_NAME environment variable is not set. Exiting.")
        raise ValueError("GCS_BUCKET_NAME environment variable is required.")

    print(f"ℹ️ Using GCS bucket: {gcs_bucket_name}")

    try:
        # Initialize the analyzer to use the specified GCS bucket
        analyzer = BitcoinATHAnalyzer(
            gcs_bucket_name=gcs_bucket_name,
            data_cache_file='bitcoin_data_cache.csv'
        )
        
        # Perform an incremental update of the data cache
        # This function handles both full downloads and incremental updates automatically.
        print("ℹ️ Calling download_bitcoin_data to update cache...")
        analyzer.download_bitcoin_data()
        
        print("✅ Scheduled daily data update job completed successfully.")
        
    except Exception as e:
        print(f"❌ An error occurred during the data update process: {e}")
        # Re-raise the exception to ensure the job execution is marked as failed in Cloud Run
        raise

if __name__ == "__main__":
    main() 