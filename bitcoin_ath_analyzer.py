import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from scipy import stats
import warnings
import os
import json
import io
from google.cloud import storage

warnings.filterwarnings('ignore')

class BitcoinATHAnalyzer:
    """
    A tool to analyze Bitcoin's distance from all-time high and contextualize
    current price action within historical distributions.
    """
    
    def __init__(self, data_cache_file='bitcoin_data_cache.csv', gcs_bucket_name=None):
        self.data = None
        self.ath_data = None
        self.gcs_bucket_name = gcs_bucket_name
        self.cache_file_name = data_cache_file  # Used for local file and GCS blob name

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
        Cache can be local or on GCS.
        
        Args:
            start_date (str): Start date in YYYY-MM-DD format
            end_date (str): End date in YYYY-MM-DD format (None for today)
            force_refresh (bool): If True, ignore cache and download fresh data
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y-%m-%d')
            
        # Check if cache exists (GCS or local)
        cache_exists = self._blob_exists() if self.bucket else os.path.exists(self.cache_file_name)
            
        if cache_exists and not force_refresh:
            print("Loading cached data...")
            cached_data = self._read_from_gcs() if self.bucket else pd.read_csv(self.cache_file_name, index_col=0, parse_dates=True)
            
            # Check if we need to update with new data
            last_cached_date = cached_data.index[-1].strftime('%Y-%m-%d')
            yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
            
            if last_cached_date >= yesterday:
                print(f"Cache is up to date (last date: {last_cached_date})")
                self.data = cached_data
                return self.data
            else:
                print(f"Updating cache from {last_cached_date} to {end_date}...")
                # Download only new data
                new_start = (pd.to_datetime(last_cached_date) + timedelta(days=1)).strftime('%Y-%m-%d')
                new_data = self._fetch_data(new_start, end_date)
                
                if not new_data.empty:
                    # Combine cached and new data
                    self.data = pd.concat([cached_data, new_data])
                    self.data = self.data[~self.data.index.duplicated(keep='last')]  # Remove duplicates
                    self._save_cache()
                    print(f"Updated cache with {len(new_data)} new days")
                else:
                    print("No new data to add")
                    self.data = cached_data
                return self.data
        else:
            print(f"Downloading Bitcoin data from {start_date} to {end_date}...")
            self.data = self._fetch_data(start_date, end_date)
            self._save_cache()
            return self.data
    
    def _fetch_data(self, start_date, end_date):
        """Fetch data from yfinance API"""
        btc = yf.Ticker("BTC-USD")
        data = btc.history(start=start_date, end=end_date)
        
        if data.empty:
            raise ValueError("No data downloaded. Check your date range and internet connection.")
            
        print(f"Successfully downloaded {len(data)} days of Bitcoin data")
        return data
    
    def _save_cache(self):
        """Save current data to cache file (local or GCS)"""
        if self.data is not None:
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
        Calculate the all-time high for each day and the percentage distance from ATH.
        """
        if self.data is None:
            raise ValueError("No data available. Please download data first.")
            
        # Create a copy for processing
        df = self.data.copy()
        
        # Calculate rolling all-time high (cumulative maximum of High prices)
        df['ATH'] = df['High'].cummax()
        
        # Calculate distance from ATH as percentage
        df['Distance_from_ATH_Pct'] = ((df['ATH'] - df['High']) / df['ATH']) * 100
        
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
        print(f"Calculated ATH distances for {len(df)} days")
        return df
    
    def get_current_percentile(self, current_distance=None):
        """
        Get the percentile rank of current distance from ATH.
        
        Args:
            current_distance (float): Current distance from ATH in percentage.
                                    If None, uses the most recent data point.
        """
        if self.ath_data is None:
            raise ValueError("ATH data not calculated. Run calculate_ath_distances() first.")
            
        if current_distance is None:
            current_distance = self.ath_data['Distance_from_ATH_Pct'].iloc[-1]
            
        # Calculate percentile rank
        percentile = stats.percentileofscore(
            self.ath_data['Distance_from_ATH_Pct'], 
            current_distance, 
            kind='rank'
        )
        
        return percentile, current_distance
    
    def analyze_distribution(self):
        """
        Analyze the distribution of distances from ATH.
        """
        if self.ath_data is None:
            raise ValueError("ATH data not calculated. Run calculate_ath_distances() first.")
            
        distances = self.ath_data['Distance_from_ATH_Pct']
        
        analysis = {
            'mean': distances.mean(),
            'median': distances.median(),
            'std': distances.std(),
            'min': distances.min(),
            'max': distances.max(),
            'percentiles': {
                '10th': distances.quantile(0.1),
                '25th': distances.quantile(0.25),
                '75th': distances.quantile(0.75),
                '90th': distances.quantile(0.9),
                '95th': distances.quantile(0.95),
                '99th': distances.quantile(0.99)
            },
            'days_at_ath': (distances == 0).sum(),
            'total_days': len(distances)
        }
        
        return analysis
    
    def plot_analysis(self, figsize=(15, 10)):
        """
        Create comprehensive visualizations of the ATH distance analysis.
        """
        if self.ath_data is None:
            raise ValueError("ATH data not calculated. Run calculate_ath_distances() first.")
            
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Bitcoin All-Time High Distance Analysis', fontsize=16, fontweight='bold')
        
        # 1. Time series of distance from ATH
        ax1 = axes[0, 0]
        ax1.plot(self.ath_data.index, self.ath_data['Distance_from_ATH_Pct'], 
                linewidth=0.8, alpha=0.8, color='#F7931A')
        ax1.set_title('Distance from ATH Over Time')
        ax1.set_ylabel('Distance from ATH (%)')
        ax1.grid(True, alpha=0.3)
        ax1.tick_params(axis='x', rotation=45)
        
        # 2. Distribution histogram
        ax2 = axes[0, 1]
        distances = self.ath_data['Distance_from_ATH_Pct']
        ax2.hist(distances, bins=50, alpha=0.7, color='#F7931A', edgecolor='black')
        ax2.axvline(distances.mean(), color='red', linestyle='--', 
                   label=f'Mean: {distances.mean():.1f}%')
        ax2.axvline(distances.median(), color='green', linestyle='--', 
                   label=f'Median: {distances.median():.1f}%')
        ax2.set_title('Distribution of Distance from ATH')
        ax2.set_xlabel('Distance from ATH (%)')
        ax2.set_ylabel('Number of Days')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. Cumulative distribution
        ax3 = axes[1, 0]
        sorted_distances = np.sort(distances)
        cumulative_pct = np.arange(1, len(sorted_distances) + 1) / len(sorted_distances) * 100
        ax3.plot(sorted_distances, cumulative_pct, color='#F7931A', linewidth=2)
        ax3.set_title('Cumulative Distribution')
        ax3.set_xlabel('Distance from ATH (%)')
        ax3.set_ylabel('Cumulative Percentage')
        ax3.grid(True, alpha=0.3)
        
        # Add current position if available
        current_distance = distances.iloc[-1]
        current_percentile = stats.percentileofscore(distances, current_distance, kind='rank')
        ax3.axvline(current_distance, color='red', linestyle='--', 
                   label=f'Current: {current_distance:.1f}% ({current_percentile:.1f}th percentile)')
        ax3.legend()
        
        # 4. Box plot by year
        ax4 = axes[1, 1]
        self.ath_data['Year'] = self.ath_data.index.year
        years_data = [self.ath_data[self.ath_data['Year'] == year]['Distance_from_ATH_Pct'] 
                     for year in sorted(self.ath_data['Year'].unique())]
        bp = ax4.boxplot(years_data, labels=sorted(self.ath_data['Year'].unique()), 
                        patch_artist=True)
        
        # Color the boxes
        for patch in bp['boxes']:
            patch.set_facecolor('#F7931A')
            patch.set_alpha(0.7)
            
        ax4.set_title('Distance from ATH by Year')
        ax4.set_xlabel('Year')
        ax4.set_ylabel('Distance from ATH (%)')
        ax4.tick_params(axis='x', rotation=45)
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    def get_context_report(self, current_distance=None):
        """
        Generate a comprehensive report contextualizing current position.
        """
        percentile, distance = self.get_current_percentile(current_distance)
        analysis = self.analyze_distribution()
        
        report = f"""
        Bitcoin All-Time High Distance Analysis Report
        =============================================
        
        Current Analysis:
        - Current distance from ATH: {distance:.2f}%
        - This puts us in the {percentile:.1f}th percentile
        - Only {percentile:.1f}% of days have been closer to ATH
        - {100-percentile:.1f}% of days have been further from ATH
        
        Historical Context:
        - Average distance from ATH: {analysis['mean']:.2f}%
        - Median distance from ATH: {analysis['median']:.2f}%
        - Days spent at ATH: {analysis['days_at_ath']} out of {analysis['total_days']} ({analysis['days_at_ath']/analysis['total_days']*100:.2f}%)
        
        Distribution Breakdown:
        - 10% of days: ≤ {analysis['percentiles']['10th']:.2f}% from ATH
        - 25% of days: ≤ {analysis['percentiles']['25th']:.2f}% from ATH  
        - 75% of days: ≤ {analysis['percentiles']['75th']:.2f}% from ATH
        - 90% of days: ≤ {analysis['percentiles']['90th']:.2f}% from ATH
        - 95% of days: ≤ {analysis['percentiles']['95th']:.2f}% from ATH
        
        Interpretation:
        """
        
        if percentile < 10:
            report += "- EXTREMELY RARE: Bitcoin is very close to ATH - this happens less than 10% of the time"
        elif percentile < 25:
            report += "- RARE: Bitcoin is unusually close to ATH - this happens less than 25% of the time"
        elif percentile < 50:
            report += "- ABOVE AVERAGE: Bitcoin is closer to ATH than usual"
        elif percentile < 75:
            report += "- TYPICAL: Bitcoin distance from ATH is in the normal range"
        else:
            report += "- FAR FROM ATH: Bitcoin is further from ATH than usual - potential opportunity?"
            
        return report

    def update_cache_incrementally(self):
        """
        Efficiently updates the data cache by fetching only new data since the
        last recorded entry.
        """
        if not self._cache_exists():
            print("Cache not found. Performing full data download.")
            self.download_bitcoin_data()
            return

        print("Cache found. Performing incremental update.")
        self.data = self._load_data_from_cache()
        last_date = pd.to_datetime(self.data['Date']).max()
        today = pd.to_datetime('today').normalize()

        if last_date >= today:
            print("✅ Data is already up-to-date. No update needed.")
            return

        start_date = last_date + pd.Timedelta(days=1)
        print(f"Fetching new data from {start_date.strftime('%Y-%m-%d')} to {today.strftime('%Y-%m-%d')}...")

        try:
            new_data = yf.download('BTC-USD', start=start_date, progress=False)
            new_data.reset_index(inplace=True)
            
            if new_data.empty:
                print("No new data found from yfinance.")
                return

            # Ensure 'Date' column is in datetime format for proper merging
            new_data['Date'] = pd.to_datetime(new_data['Date']).dt.normalize()

            # Combine, remove any potential duplicates, and sort
            combined_data = pd.concat([self.data, new_data]).drop_duplicates(subset=['Date'], keep='last')
            self.data = combined_data.sort_values(by='Date').reset_index(drop=True)
            
            # Reprocess all data to ensure ATH is calculated correctly with new values
            self.load_data(process=True)
            
            self._save_data_to_cache(self.data)
            print(f"✅ Data cache successfully updated with {len(new_data)} new row(s).")

        except Exception as e:
            print(f"❌ Failed to update data: {e}")


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
    recent_cols = ['High', 'ATH', 'Distance_from_ATH_Pct', 'Days_Since_ATH']
    print(analyzer.ath_data[recent_cols].tail(10).round(2))


if __name__ == "__main__":
    main() 