import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
import warnings
import os
import tempfile
import io
from google.cloud import storage

# Import the reliable API client
from api_integrations import BitcoinPriceAPI

warnings.filterwarnings('ignore')

class BitcoinATHAnalyzer:
    """
    A tool to analyze Bitcoin's distance from all-time high and contextualize
    current price action within historical distributions.
    """
    
    def __init__(self, data_cache_file='bitcoin_data_cache.csv', gcs_bucket_name=None):
        # Set yfinance cache to a temporary directory to avoid issues in
        # read-only environments like Cloud Run.
        yf.set_tz_cache_location(os.path.join(tempfile.gettempdir(), 'yfinance_cache'))
        
        self.data = None
        self.ath_data = None
        self.gcs_bucket_name = gcs_bucket_name
        self.cache_file_name = data_cache_file  # Used for local file and GCS blob name
        
        # Use our reliable API client
        self.price_api = BitcoinPriceAPI()

        if self.gcs_bucket_name:
            self.storage_client = storage.Client()
            self.bucket = self.storage_client.bucket(self.gcs_bucket_name)
        else:
            # Fallback to local file for development if no bucket is provided
            self.bucket = None
        
    def _read_from_gcs(self):
        """Reads data from GCS blob into a pandas DataFrame."""
        blob = self.bucket.blob(self.cache_file_name)
        try:
            data_bytes = blob.download_as_bytes()
            return pd.read_csv(io.BytesIO(data_bytes), index_col=0, parse_dates=True)
        except Exception as e:
            print(f"Failed to download from GCS: {e}")
            return None

    def _blob_exists(self):
        """Checks if the GCS blob exists."""
        blob = self.bucket.blob(self.cache_file_name)
        return blob.exists()

    def download_bitcoin_data(self, start_date='2010-01-01', end_date=None, force_refresh=False):
        """
        Download Bitcoin historical data using yfinance with caching support.
        Uses comprehensive dataset if available, otherwise falls back to yfinance.
        Cache can be local or on GCS.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format (None for today)
            force_refresh (bool): If True, ignore cache and download fresh data
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # Check if cache exists (GCS or local)
        gcs_cache_exists = self._blob_exists() if self.bucket else False
        local_cache_exists = os.path.exists(self.cache_file_name)
            
        if (gcs_cache_exists or local_cache_exists) and not force_refresh:
            print("Loading cached comprehensive data...")
            
            # Prioritize GCS cache if it exists
            if gcs_cache_exists:
                cached_data = self._read_from_gcs()
                cache_source = "GCS"
            else:
                cached_data = pd.read_csv(self.cache_file_name, index_col=0, parse_dates=True)
                cache_source = "local"
            
            if cached_data is None:
                print(f"Failed to load cached data from {cache_source}, trying alternative...")
                
                # If GCS failed, try local
                if cache_source == "GCS" and local_cache_exists:
                    print("Trying local cache...")
                    cached_data = pd.read_csv(self.cache_file_name, index_col=0, parse_dates=True)
                    cache_source = "local"
                
                # If still no data, fall back to downloading
                if cached_data is None:
                    print("No cached data available, downloading fresh data...")
                    self.data = self._fetch_historical_data_yfinance(start_date, end_date)
                    self._save_cache()
                    return self.data
            
            print(f"Loaded {len(cached_data)} days from {cache_source} cache")
            
            # If we loaded from local cache and have GCS, upload to GCS
            if cache_source == "local" and self.bucket:
                print("Uploading local comprehensive data to GCS...")
                self.data = cached_data
                self._save_cache()  # This will upload to GCS
            else:
                self.data = cached_data
            
            # Check if we need to update with new data
            last_cached_date = cached_data.index[-1].strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            if last_cached_date >= yesterday:
                print(f"Cache is up to date (last date: {last_cached_date})")
                return self.data
            else:
                print(f"Updating cache from {last_cached_date} to {end_date}...")
                # For incremental updates, use the reliable CoinGecko API.
                new_data = self._fetch_incremental_data_coingecko()
                
                if not new_data.empty:
                    # Combine cached and new data
                    self.data = pd.concat([self.data, new_data])
                    self.data = self.data[~self.data.index.duplicated(keep='last')]  # Remove duplicates
                    self._save_cache()
                    print(f"Updated cache with {len(new_data)} new days")
                else:
                    print("No new data to add from CoinGecko")
                return self.data
        else:
            print(f"No comprehensive cache found. Using yfinance for historical download...")
            self.data = self._fetch_historical_data_yfinance(start_date, end_date)
            self._save_cache()
            return self.data

    def _fetch_historical_data_yfinance(self, start_date, end_date):
        """Fetch full historical data from yfinance API."""
        try:
            print(f"Attempting to fetch data for BTC-USD from {start_date} to {end_date}")
            btc = yf.Ticker("BTC-USD")
            data = btc.history(start=start_date, end=end_date)
            
            if data.empty:
                raise ValueError("yfinance returned an empty DataFrame. This may indicate a network issue or an API block.")
                
            print(f"Successfully downloaded {len(data)} days of Bitcoin data")
            return data
        except Exception as e:
            print(f"An exception occurred while fetching data from yfinance: {e}")
            raise ValueError(f"No data downloaded. Underlying error: {e}")

    def _fetch_incremental_data_coingecko(self, days=7):
        """Fetch recent data from CoinGecko API (for reliable daily updates)."""
        try:
            print(f"Attempting to fetch recent {days} days from CoinGecko...")
            data = self.price_api.get_daily_ohlcv_coingecko(days=days)

            if data.empty:
                raise ValueError("CoinGecko API returned an empty DataFrame.")
            
            if 'Volume' not in data.columns:
                data['Volume'] = 0

            print(f"Successfully downloaded {len(data)} days of Bitcoin data from CoinGecko")
            return data
        except Exception as e:
            print(f"An exception occurred while fetching data from CoinGecko: {e}")
            # In case of failure, it's better to continue with stale data than to crash.
            # Return an empty DataFrame to signify that no new data was added.
            return pd.DataFrame()
    
    def _save_cache(self):
        """Save current data to cache file (local or GCS)"""
        if self.data is not None:
            # Add a validation step to prevent writing future-dated or incomplete daily data to the cache.
            today = pd.to_datetime('today', utc=True).normalize()
            original_rows = len(self.data)
            
            # Filter to include only data for days that have already closed (i.e., before today).
            self.data = self.data[self.data.index < today]
            new_rows = len(self.data)
            
            if new_rows < original_rows:
                rows_removed = original_rows - new_rows
                print(f"⚠️  Removed {rows_removed} rows (future-dated or current day) before caching.")

            if self.bucket:
                blob = self.bucket.blob(self.cache_file_name)
                csv_buffer = io.StringIO()
                self.data.to_csv(csv_buffer)
                blob.upload_from_string(csv_buffer.getvalue(), content_type='text/csv')
                print(f"Data cached to GCS: gs://{self.gcs_bucket_name}/{self.cache_file_name}")
            else:
                self.data.to_csv(self.cache_file_name)
                print(f"Data cached to {self.cache_file_name}")
    
    def clear_cache(self):
        """Clear the cached data file (local or GCS)"""
        if self.bucket:
            blob = self.bucket.blob(self.cache_file_name)
            if blob.exists():
                blob.delete()
                print(f"Cache removed from GCS: gs://{self.gcs_bucket_name}/{self.cache_file_name}")
        elif os.path.exists(self.cache_file_name):
            os.remove(self.cache_file_name)
            print(f"Cache file {self.cache_file_name} removed")
    
    def calculate_ath_distances(self):
        """
        Calculate the all-time high for each day and the percentage of previous ATH.
        
        Uses the ATH up to and including the day before, allowing days that break
        the ATH to show >100% and better capture the emotional experience.
        """
        if self.data is None:
            raise ValueError("No data available. Please download data first.")
            
        # Create a copy for processing
        df = self.data.copy()
        
        # Calculate rolling all-time high up to and including the day before
        # This allows days that break ATH to show >100%
        df['ATH'] = df['High'].shift(1).cummax()
        
        # For the first day, use the first day's high as the ATH
        # (since there's no previous day to compare against)
        df['ATH'].iloc[0] = df['High'].iloc[0]
        
        # Calculate percent of ATH as percentage (inverse of distance from ATH)
        df['Percent_of_ATH'] = (df['High'] / df['ATH']) * 100
        
        # Add some additional useful metrics
        df['Days_Since_ATH'] = 0
        df['Is_ATH'] = df['High'] == df['ATH']
        
        # Calculate days since last ATH
        ath_dates = df[df['Is_ATH']].index
        for i, date in enumerate(df.index):
            last_ath_dates = ath_dates[ath_dates <= date]
            if len(last_ath_dates) > 0:
                days_since = (date - last_ath_dates[-1]).days
                df.loc[date, 'Days_Since_ATH'] = days_since
        
        self.ath_data = df
        print(f"Calculated ATH percentages for {len(df)} days")
        return df
    
    def get_current_percentile(self, current_percent=None):
        """
        Get the percentile rank of current percent of ATH.
        
        Args:
            current_percent (float): Current percent of ATH.
                                   If None, uses the most recent data point.
        """
        if self.ath_data is None:
            raise ValueError("ATH data not calculated. Run calculate_ath_distances() first.")
            
        if current_percent is None:
            current_percent = self.ath_data['Percent_of_ATH'].iloc[-1]
            
        # Calculate percentile rank
        percentile = stats.percentileofscore(
            self.ath_data['Percent_of_ATH'], 
            current_percent, 
            kind='rank'
        )
        
        return percentile, current_percent
    
    def analyze_distribution(self):
        """
        Analyze the distribution of percent of ATH.
        """
        if self.ath_data is None:
            raise ValueError("ATH data not calculated. Run calculate_ath_distances() first.")
            
        percentages = self.ath_data['Percent_of_ATH']
        
        analysis = {
            'mean': percentages.mean(),
            'median': percentages.median(),
            'std': percentages.std(),
            'min': percentages.min(),
            'max': percentages.max(),
            'percentiles': {
                '10th': percentages.quantile(0.1),
                '25th': percentages.quantile(0.25),
                '75th': percentages.quantile(0.75),
                '90th': percentages.quantile(0.9),
                '95th': percentages.quantile(0.95),
                '99th': percentages.quantile(0.99)
            },
            'days_at_ath': (percentages == 100).sum(),
            'days_above_ath': (percentages > 100).sum(),
            'days_at_or_above_ath': (percentages >= 100).sum(),
            'total_days': len(percentages)
        }
        
        return analysis
    
    def plot_analysis(self, figsize=(15, 10)):
        """
        Create comprehensive visualizations of the percent of ATH analysis.
        """
        if self.ath_data is None:
            raise ValueError("ATH data not calculated. Run calculate_ath_distances() first.")
            
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Bitcoin Percent of All-Time High Analysis', fontsize=16, fontweight='bold')
        
        # 1. Time series of percent of ATH
        ax1 = axes[0, 0]
        ax1.plot(self.ath_data.index, self.ath_data['Percent_of_ATH'], 
                linewidth=0.8, alpha=0.8, color='#F7931A')
        ax1.set_title('Percent of ATH Over Time')
        ax1.set_ylabel('Percent of ATH (%)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Distribution histogram
        ax2 = axes[0, 1]
        percentages = self.ath_data['Percent_of_ATH']
        ax2.hist(percentages, bins=50, alpha=0.7, color='#F7931A', edgecolor='black')
        ax2.axvline(percentages.mean(), color='red', linestyle='--', 
                   label=f'Mean: {percentages.mean():.1f}%')
        ax2.axvline(percentages.median(), color='green', linestyle='--', 
                   label=f'Median: {percentages.median():.1f}%')
        ax2.set_title('Distribution of Percent of ATH')
        ax2.set_xlabel('Percent of ATH (%)')
        ax2.set_ylabel('Number of Days')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Cumulative distribution
        ax3 = axes[1, 0]
        sorted_percentages = np.sort(percentages)
        cumulative_pct = np.arange(1, len(sorted_percentages) + 1) / len(sorted_percentages) * 100
        ax3.plot(sorted_percentages, cumulative_pct, color='#F7931A', linewidth=2)
        ax3.set_title('Cumulative Distribution')
        ax3.set_xlabel('Percent of ATH (%)')
        ax3.set_ylabel('Cumulative Percentage')
        ax3.grid(True, alpha=0.3)
        
        # Add current position if available
        current_percent = percentages.iloc[-1]
        current_percentile = stats.percentileofscore(percentages, current_percent, kind='rank')
        ax3.axvline(current_percent, color='red', linestyle='--', 
                   label=f'Current: {current_percent:.1f}% ({current_percentile:.1f}th percentile)')
        ax3.legend()
        
        # 4. Box plot by year
        ax4 = axes[1, 1]
        self.ath_data['Year'] = self.ath_data.index.year
        years_data = [self.ath_data[self.ath_data['Year'] == year]['Percent_of_ATH'] 
                     for year in sorted(self.ath_data['Year'].unique())]
        bp = ax4.boxplot(years_data, labels=sorted(self.ath_data['Year'].unique()), 
                        patch_artist=True)
        
        # Color the boxes
        for patch in bp['boxes']:
            patch.set_facecolor('#F7931A')
            patch.set_alpha(0.7)
            
        ax4.set_title('Percent of ATH by Year')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Percent of ATH (%)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def get_context_report(self, current_percent=None):
        """
        Generate a comprehensive report contextualizing current position.
        """
        percentile, percent = self.get_current_percentile(current_percent)
        analysis = self.analyze_distribution()
        
        report = f"""
        Bitcoin Percent of All-Time High Analysis Report
        =================================================
        
        Current Analysis:
        - Current percent of ATH: {percent:.2f}%
        - This puts us in the {percentile:.1f}th percentile
        - {percentile:.1f}% of days have been lower than today
        - {100-percentile:.1f}% of days have been higher than today
        
        Historical Context:
        - Average percent of ATH: {analysis['mean']:.2f}%
        - Median percent of ATH: {analysis['median']:.2f}%
        - Days spent at ATH (=100%): {analysis['days_at_ath']} out of {analysis['total_days']} ({analysis['days_at_ath']/analysis['total_days']*100:.2f}%)
        - Days above ATH (>100%): {analysis['days_above_ath']} out of {analysis['total_days']} ({analysis['days_above_ath']/analysis['total_days']*100:.2f}%)
        - Days at or above ATH (≥100%): {analysis['days_at_or_above_ath']} out of {analysis['total_days']} ({analysis['days_at_or_above_ath']/analysis['total_days']*100:.2f}%)
        
        Distribution Breakdown:
        - 10% of days: ≤ {analysis['percentiles']['10th']:.2f}% of ATH
        - 25% of days: ≤ {analysis['percentiles']['25th']:.2f}% of ATH  
        - 75% of days: ≤ {analysis['percentiles']['75th']:.2f}% of ATH
        - 90% of days: ≤ {analysis['percentiles']['90th']:.2f}% of ATH
        - 95% of days: ≤ {analysis['percentiles']['95th']:.2f}% of ATH
        
        Interpretation:
        """
        
        if percent > 100:
            report += f"- NEW ATH TERRITORY: Bitcoin broke the previous ATH by {percent-100:.1f}% - this is rare!"
        elif percentile > 90:
            report += "- EXTREMELY HIGH: Bitcoin is very close to ATH - this happens less than 10% of the time"
        elif percentile > 75:
            report += "- HIGH: Bitcoin is unusually close to ATH - this happens less than 25% of the time"
        elif percentile > 50:
            report += "- ABOVE AVERAGE: Bitcoin is closer to ATH than usual"
        elif percentile > 25:
            report += "- TYPICAL: Bitcoin percent of ATH is in the normal range"
        else:
            report += "- FAR FROM ATH: Bitcoin is further from ATH than usual - potential opportunity?"
            
        return report

def main():
    """
    Example usage of the BitcoinATHAnalyzer
    """
    # Initialize analyzer
    analyzer = BitcoinATHAnalyzer()
    
    # Download data (going back as far as possible)
    try:
        analyzer.download_bitcoin_data(start_date='2010-01-01')
    except Exception as e:
        print(f"Error downloading data: {e}")
        return
    
    # Calculate ATH distances
    analyzer.calculate_ath_distances()
    
    # Generate and print report
    report = analyzer.get_context_report()
    print(report)
    
    # Create visualizations
    analyzer.plot_analysis()
    
    # Show recent data
    print("\nRecent 10 days of data:")
    recent_cols = ['High', 'ATH', 'Percent_of_ATH', 'Days_Since_ATH']
    print(analyzer.ath_data[recent_cols].tail(10).round(2))


if __name__ == "__main__":
    main() 