#!/usr/bin/env python3
"""
Comprehensive Bitcoin Data Rebuilder
Rebuilds the complete Bitcoin historical dataset (2010-present) from authoritative sources.

This script is the definitive way to recreate your comprehensive Bitcoin data if ever lost.
It combines:
1. Historical data from GitHub repository (2010-2022) - Mt. Gox, Bitstamp, Coinbase  
2. Current data from yfinance (2022-present)
3. Proper merging with historical data taking precedence where overlaps exist

Usage:
    python rebuild_comprehensive_data.py
    
Output: 
    bitcoin_data_cache.csv (ready for BitcoinATHAnalyzer)
"""

import os
import sys
import json
import pandas as pd
import requests
import subprocess
from datetime import datetime
import tempfile
import shutil

class ComprehensiveDataRebuilder:
    def __init__(self):
        self.temp_dir = None
        self.historical_df = None
        self.current_df = None
        self.final_df = None
        
    def log(self, message):
        """Simple logging with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] {message}")
        
    def setup_temp_directory(self):
        """Create temporary directory for processing"""
        self.temp_dir = tempfile.mkdtemp(prefix='bitcoin_rebuild_')
        self.log(f"📁 Created temp directory: {self.temp_dir}")
        
    def cleanup_temp_directory(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
            self.log("🧹 Cleaned up temporary files")
            
    def download_historical_data(self):
        """Download historical Bitcoin data from GitHub repository (2010-2022)"""
        self.log("📊 Downloading historical Bitcoin data (2010-2022)...")
        
        # Clone the full Bitcoin price history repository
        repo_url = "https://github.com/cilphex/full-bitcoin-price-history.git"
        repo_path = os.path.join(self.temp_dir, "full-bitcoin-price-history")
        
        try:
            result = subprocess.run(['git', 'clone', repo_url, repo_path], 
                                  capture_output=True, text=True, check=True)
            self.log("✅ Successfully cloned historical data repository")
        except subprocess.CalledProcessError as e:
            self.log(f"❌ Failed to clone repository: {e}")
            return None
            
        # Load and process the aggregate data
        aggregate_file = os.path.join(repo_path, 'price-data', 'aggregate-data.json')
        
        if not os.path.exists(aggregate_file):
            self.log(f"❌ Aggregate data file not found: {aggregate_file}")
            return None
            
        try:
            with open(aggregate_file, 'r') as f:
                data = json.load(f)
                
            candles = data.get('candles', [])
            if not candles:
                self.log("❌ No candles data found in JSON")
                return None
                
            # Convert to DataFrame
            df_data = []
            for entry in candles:
                if len(entry) >= 5:
                    try:
                        timestamp = pd.to_datetime(entry[0], unit='s', utc=True)
                        row = {
                            'Open': float(entry[1]) if entry[1] else None,
                            'High': float(entry[2]) if entry[2] else None,
                            'Low': float(entry[3]) if entry[3] else None,
                            'Close': float(entry[4]) if entry[4] else None,
                            'Volume': float(entry[5]) if len(entry) > 5 and entry[5] else 0.0
                        }
                        
                        if row['Close'] and row['Close'] > 0:
                            df_data.append((timestamp, row))
                    except (ValueError, TypeError):
                        continue
                        
            if not df_data:
                self.log("❌ No valid historical data found")
                return None
                
            # Create DataFrame
            timestamps, rows = zip(*df_data)
            self.historical_df = pd.DataFrame(list(rows), index=timestamps)
            
            # Fill missing OHLC values with Close price
            for col in ['Open', 'High', 'Low']:
                self.historical_df[col] = self.historical_df[col].fillna(self.historical_df['Close'])
                
            # Remove any remaining NaN values
            self.historical_df = self.historical_df.dropna()
            
            self.log(f"✅ Processed {len(self.historical_df)} days of historical data")
            self.log(f"📅 Historical range: {self.historical_df.index.min().strftime('%Y-%m-%d')} to {self.historical_df.index.max().strftime('%Y-%m-%d')}")
            self.log(f"💰 Historical price range: ${self.historical_df['Close'].min():.4f} to ${self.historical_df['Close'].max():.2f}")
            
            return self.historical_df
            
        except Exception as e:
            self.log(f"❌ Error processing historical data: {e}")
            return None
            
    def download_current_data(self):
        """Download current Bitcoin data using yfinance"""
        self.log("📈 Downloading current Bitcoin data...")
        
        try:
            import yfinance as yf
            btc = yf.Ticker("BTC-USD")
            
            # Get data from where historical data ends to present
            historical_end = self.historical_df.index.max() if self.historical_df is not None else '2022-06-01'
            start_date = historical_end.strftime('%Y-%m-%d') if hasattr(historical_end, 'strftime') else historical_end
            
            self.current_df = btc.history(start=start_date)
            
            if self.current_df.empty:
                self.log("⚠️  No current data downloaded, using historical only")
                return self.historical_df
                
            self.log(f"✅ Downloaded {len(self.current_df)} days of current data")
            self.log(f"📅 Current range: {self.current_df.index.min().strftime('%Y-%m-%d')} to {self.current_df.index.max().strftime('%Y-%m-%d')}")
            
            return self.current_df
            
        except Exception as e:
            self.log(f"❌ Error downloading current data: {e}")
            return None
            
    def merge_datasets(self):
        """Merge historical and current data with historical taking precedence"""
        self.log("🔗 Merging historical and current datasets...")
        
        if self.historical_df is None:
            self.log("❌ No historical data to merge")
            return None
            
        if self.current_df is None or self.current_df.empty:
            self.log("ℹ️  No current data, using historical only")
            self.final_df = self.historical_df
            
        else:
            # Find overlap and prioritize historical data
            historical_end = self.historical_df.index.max()
            current_unique = self.current_df[self.current_df.index > historical_end]
            
            if not current_unique.empty:
                self.final_df = pd.concat([self.historical_df, current_unique])
                self.final_df = self.final_df.sort_index()
                self.log(f"✅ Merged datasets: {len(self.final_df)} total days")
            else:
                self.final_df = self.historical_df
                self.log("ℹ️  No unique current data to add")
                
        # Final data validation
        self.log(f"📊 Final dataset: {len(self.final_df)} days")
        self.log(f"📅 Full range: {self.final_df.index.min().strftime('%Y-%m-%d')} to {self.final_df.index.max().strftime('%Y-%m-%d')}")
        self.log(f"💰 Full price range: ${self.final_df['Close'].min():.4f} to ${self.final_df['Close'].max():.2f}")
        
        return self.final_df
        
    def save_final_dataset(self, output_file='bitcoin_data_cache.csv'):
        """Save the final comprehensive dataset"""
        if self.final_df is None:
            self.log("❌ No final dataset to save")
            return False
            
        try:
            self.final_df.to_csv(output_file)
            self.log(f"✅ Saved comprehensive dataset as '{output_file}'")
            
            # Show key milestones
            self.log("🏆 Key Bitcoin milestones in dataset:")
            milestones = [0.1, 1, 10, 100, 1000, 10000]
            for price in milestones:
                milestone_data = self.final_df[self.final_df['High'] >= price]
                if not milestone_data.empty:
                    first_date = milestone_data.index[0]
                    first_high = milestone_data.iloc[0]['High']
                    self.log(f"   ${price:g}: {first_date.strftime('%Y-%m-%d')} (High: ${first_high:.4f})")
                    
            return True
            
        except Exception as e:
            self.log(f"❌ Error saving dataset: {e}")
            return False
            
    def rebuild(self, output_file='bitcoin_data_cache.csv'):
        """Main rebuild process"""
        self.log("🚀 Starting comprehensive Bitcoin data rebuild...")
        self.log("=" * 70)
        
        try:
            # Setup
            self.setup_temp_directory()
            
            # Download and process data
            if self.download_historical_data() is None:
                self.log("❌ Failed to download historical data")
                return False
                
            if self.download_current_data() is None:
                self.log("⚠️  Failed to download current data, continuing with historical only")
                
            # Merge and save
            if self.merge_datasets() is None:
                self.log("❌ Failed to merge datasets")
                return False
                
            success = self.save_final_dataset(output_file)
            
            if success:
                self.log("=" * 70)
                self.log("🎉 Comprehensive Bitcoin dataset rebuild COMPLETE!")
                self.log(f"📁 Output file: {output_file}")
                self.log("🔧 Ready for use with BitcoinATHAnalyzer")
                
            return success
            
        except Exception as e:
            self.log(f"❌ Rebuild failed: {e}")
            return False
            
        finally:
            self.cleanup_temp_directory()

def main():
    """Main entry point"""
    print("🚀 Comprehensive Bitcoin Data Rebuilder")
    print("This will rebuild your complete Bitcoin dataset from 2010 to present")
    print("Sources: GitHub historical repo (2010-2022) + yfinance (current)")
    print()
    
    rebuilder = ComprehensiveDataRebuilder()
    success = rebuilder.rebuild()
    
    if success:
        print("\n✅ SUCCESS! Your comprehensive Bitcoin dataset is ready.")
        print("   File: bitcoin_data_cache.csv")
        print("   Usage: analyzer = BitcoinATHAnalyzer(); analyzer.download_bitcoin_data()")
    else:
        print("\n❌ FAILED! Check the logs above for errors.")
        sys.exit(1)

if __name__ == "__main__":
    main() 