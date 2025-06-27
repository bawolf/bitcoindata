"""
Production-ready API integrations for Bitcoin price data.
Designed for daily updates and real-time price tracking.
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import time
from typing import Dict, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BitcoinPriceAPI:
    """
    Production-ready Bitcoin price API client for current price data and daily updates
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BitcoinATHAnalyzer/1.0 (Educational Project)'
        })
    
    def get_current_price_coingecko(self) -> Dict:
        """
        Get current Bitcoin price from CoinGecko API (FREE, reliable)
        
        Returns:
            Dict with current price, 24h high, market data
        """
        try:
            # Use simple price endpoint first
            url = "https://api.coingecko.com/api/v3/simple/price"
            params = {
                'ids': 'bitcoin',
                'vs_currencies': 'usd',
                'include_24hr_vol': 'true',
                'include_24hr_change': 'true',
                'include_last_updated_at': 'true'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()['bitcoin']
            
            # For 24h high, try to get from OHLC endpoint (simpler than market chart)
            try:
                ohlc_url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"
                ohlc_params = {
                    'vs_currency': 'usd',
                    'days': '1'
                }
                
                ohlc_response = self.session.get(ohlc_url, params=ohlc_params, timeout=5)
                ohlc_response.raise_for_status()
                ohlc_data = ohlc_response.json()
                
                # Get today's high (most recent OHLC entry)
                if ohlc_data:
                    high_24h = max([candle[2] for candle in ohlc_data])  # candle[2] is High
                else:
                    high_24h = data['usd']
                    
            except Exception as ohlc_error:
                logger.warning(f"OHLC endpoint failed, using current price as high: {ohlc_error}")
                high_24h = data['usd']
            
            return {
                'price': data['usd'],
                'high_24h': high_24h,
                'volume_24h': data.get('usd_24h_vol', 0),
                'change_24h': data.get('usd_24h_change', 0),
                'timestamp': datetime.now(),
                'source': 'coingecko'
            }
            
        except Exception as e:
            logger.error(f"CoinGecko API error: {e}")
            raise
    
    def get_current_price_coinmarketcap(self, api_key: str) -> Dict:
        """
        Get current Bitcoin price from CoinMarketCap API (Requires API key)
        
        Args:
            api_key: CoinMarketCap API key
            
        Returns:
            Dict with current price and market data
        """
        try:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
            headers = {
                'X-CMC_PRO_API_KEY': api_key,
                'Accept': 'application/json'
            }
            params = {
                'symbol': 'BTC',
                'convert': 'USD'
            }
            
            response = self.session.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()['data']['BTC']['quote']['USD']
            
            return {
                'price': data['price'],
                'high_24h': data.get('high_24h', data['price']),  # CMC doesn't always provide 24h high
                'volume_24h': data['volume_24h'],
                'change_24h': data['percent_change_24h'],
                'timestamp': datetime.now(),
                'source': 'coinmarketcap'
            }
            
        except Exception as e:
            logger.error(f"CoinMarketCap API error: {e}")
            raise
    
    def get_daily_ohlcv_coingecko(self, days: int = 1) -> pd.DataFrame:
        """
        Get daily OHLCV data from CoinGecko (for recent daily updates)
        
        Args:
            days: Number of days to fetch (1-365)
            
        Returns:
            DataFrame with OHLCV data
        """
        try:
            url = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"
            params = {
                'vs_currency': 'usd',
                'days': days
            }
            
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            
            # Convert to DataFrame
            df = pd.DataFrame(data, columns=['timestamp', 'Open', 'High', 'Low', 'Close'])
            # Ensure the timestamp is timezone-aware (UTC) to match yfinance data
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms', utc=True)
            df.set_index('timestamp', inplace=True)
            
            return df
            
        except Exception as e:
            logger.error(f"CoinGecko OHLCV API error: {e}")
            raise
    
    def get_current_price_with_fallback(self, cmc_api_key: Optional[str] = None) -> Dict:
        """
        Get current price with fallback to multiple APIs
        
        Args:
            cmc_api_key: Optional CoinMarketCap API key for fallback
            
        Returns:
            Dict with current price data
        """
        # Try CoinGecko first (free and reliable)
        try:
            return self.get_current_price_coingecko()
        except Exception as e:
            logger.warning(f"CoinGecko failed: {e}")
        
        # Fallback to CoinMarketCap if API key provided
        if cmc_api_key:
            try:
                return self.get_current_price_coinmarketcap(cmc_api_key)
            except Exception as e:
                logger.warning(f"CoinMarketCap failed: {e}")
        
        # Final fallback to yfinance (what we use for historical data)
        try:
            import yfinance as yf
            btc = yf.Ticker("BTC-USD")
            info = btc.info
            hist = btc.history(period="1d")
            
            if not hist.empty:
                latest = hist.iloc[-1]
                return {
                    'price': latest['Close'],
                    'high_24h': latest['High'],
                    'volume_24h': latest['Volume'],
                    'change_24h': 0,  # yfinance doesn't provide this directly
                    'timestamp': datetime.now(),
                    'source': 'yfinance'
                }
        except Exception as e:
            logger.error(f"All API sources failed. Last error: {e}")
            raise Exception("All price API sources failed")


class DailyUpdateManager:
    """
    Manages daily updates for Bitcoin ATH analysis
    """
    
    def __init__(self, analyzer, price_api):
        self.analyzer = analyzer
        self.price_api = price_api
    
    def run_daily_update(self) -> Dict:
        """
        Run the daily update process
        
        Returns:
            Dict with update results
        """
        try:
            logger.info("Starting daily Bitcoin ATH analysis update...")
            
            # 1. Update historical data (only fetches new data)
            self.analyzer.download_bitcoin_data()
            
            # 2. Recalculate ATH distances
            self.analyzer.calculate_ath_distances()
            
            # 3. Get current market data
            current_data = self.price_api.get_current_price_with_fallback()
            
            # 4. Calculate current percentile and dollar difference
            current_percent = None
            dollar_difference = 0
            latest_ath = 0
            
            if len(self.analyzer.ath_data) > 0:
                latest_ath = self.analyzer.ath_data['ATH'].iloc[-1]
                current_percent = (current_data['price'] / latest_ath) * 100
                dollar_difference = latest_ath - current_data['price']
            
            percentile, percent = self.analyzer.get_current_percentile(current_percent)
            
            # 5. Generate analysis
            analysis = self.analyzer.analyze_distribution()
            
            result = {
                'success': True,
                'timestamp': datetime.now().isoformat(),
                'current_price': float(current_data['price']),
                'current_ath': float(latest_ath),
                'dollar_difference_from_ath': float(dollar_difference),
                'current_percent_of_ath': float(percent),
                'percentile_rank': float(percentile),
                'total_days_analyzed': int(len(self.analyzer.ath_data)),
                'analysis_summary': {
                    'mean_percent': float(analysis['mean']),
                    'median_percent': float(analysis['median']),
                    'days_at_ath': int(analysis['days_at_ath'])
                },
                'api_source': current_data['source']
            }
            
            logger.info(f"Daily update completed successfully. Current percent: {percent:.2f}% of ATH (percentile: {percentile:.1f})")
            return result
            
        except Exception as e:
            logger.error(f"Daily update failed: {e}")
            return {
                'success': False,
                'timestamp': datetime.now().isoformat(),
                'error': str(e)
            }

# Example usage for production website
def create_daily_update_job():
    """
    Example function for setting up a daily cron job
    """
    from bitcoin_ath_analyzer import BitcoinATHAnalyzer
    
    # Initialize components
    analyzer = BitcoinATHAnalyzer()
    price_api = BitcoinPriceAPI()
    update_manager = DailyUpdateManager(analyzer, price_api)
    
    # Run update
    result = update_manager.run_daily_update()
    
    # Log or store result for monitoring
    if result['success']:
        print(f"✅ Daily update successful: {result['current_percent_of_ath']:.2f}% of ATH")
    else:
        print(f"❌ Daily update failed: {result['error']}")
    
    return result

if __name__ == "__main__":
    # Test the API
    api = BitcoinPriceAPI()
    try:
        price_data = api.get_current_price_coingecko()
        print(f"Current BTC Price: ${price_data['price']:,.2f}")
        print(f"24h High: ${price_data['high_24h']:,.2f}")
    except Exception as e:
        print(f"API test failed: {e}") 