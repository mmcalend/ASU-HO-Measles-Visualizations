"""
Data Manager for Measles Visualization Dashboard
Handles data fetching, validation, and processing from CDC APIs with robust fallback mechanisms.
"""

import pandas as pd
import requests
import logging
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, Tuple


class DataManager:
    """Manages data fetching and processing for measles visualizations"""
    
    # API Endpoints
    TIMELINE_API = "https://data.cdc.gov/resource/qe4i-8iw7.json"
    MEASLES_API = "https://data.cdc.gov/resource/htfv-yiiy.json"
    VACCINATION_API = "https://data.cdc.gov/resource/ykpw-fhwi.json"
    
    # Alternative endpoints (fallback)
    TIMELINE_API_ALT = "https://data.cdc.gov/api/views/qe4i-8iw7/rows.json?accessType=DOWNLOAD"
    MEASLES_API_ALT = "https://data.cdc.gov/api/views/htfv-yiiy/rows.json?accessType=DOWNLOAD"
    
    # Backup data directory
    BACKUP_DIR = Path('backup_data')
    
    # Request timeout (seconds)
    TIMEOUT = 30
    
    def __init__(self):
        """Initialize DataManager"""
        self.BACKUP_DIR.mkdir(exist_ok=True)
        self.current_year = datetime.now().year
        logging.info(f"DataManager initialized. Current year: {self.current_year}")
    
    def fetch_with_fallback(self, primary_url: str, alt_url: str, backup_file: str, 
                           dataset_name: str) -> Optional[pd.DataFrame]:
        """
        Fetch data with three-tier fallback system:
        1. Primary API endpoint
        2. Alternative API endpoint
        3. Local backup CSV file
        
        Args:
            primary_url: Primary API endpoint URL
            alt_url: Alternative API endpoint URL
            backup_file: Path to backup CSV file
            dataset_name: Name of dataset for logging
            
        Returns:
            DataFrame if successful, None otherwise
        """
        # Try primary API
        try:
            logging.info(f"Fetching {dataset_name} from primary API...")
            response = requests.get(primary_url, timeout=self.TIMEOUT)
            response.raise_for_status()
            df = pd.DataFrame(response.json())
            
            if not df.empty:
                logging.info(f"✓ Successfully fetched {dataset_name}: {len(df)} records")
                # Save as backup
                self._save_backup(df, backup_file)
                return df
        except Exception as e:
            logging.warning(f"Primary API failed for {dataset_name}: {str(e)}")
        
        # Try alternative API
        try:
            logging.info(f"Trying alternative API for {dataset_name}...")
            response = requests.get(alt_url, timeout=self.TIMEOUT)
            response.raise_for_status()
            df = pd.DataFrame(response.json())
            
            if not df.empty:
                logging.info(f"✓ Successfully fetched {dataset_name} from alt API: {len(df)} records")
                self._save_backup(df, backup_file)
                return df
        except Exception as e:
            logging.warning(f"Alternative API failed for {dataset_name}: {str(e)}")
        
        # Try local backup
        try:
            backup_path = self.BACKUP_DIR / backup_file
            if backup_path.exists():
                logging.info(f"Loading {dataset_name} from backup file...")
                df = pd.read_csv(backup_path)
                logging.warning(f"⚠ Using backup data for {dataset_name}: {len(df)} records")
                return df
            else:
                logging.error(f"✗ No backup file found for {dataset_name} at {backup_path}")
        except Exception as e:
            logging.error(f"✗ Failed to load backup for {dataset_name}: {str(e)}")
        
        return None
    
    def _save_backup(self, df: pd.DataFrame, filename: str):
        """Save DataFrame as backup CSV"""
        try:
            backup_path = self.BACKUP_DIR / filename
            df.to_csv(backup_path, index=False)
            logging.info(f"Saved backup: {filename}")
        except Exception as e:
            logging.warning(f"Could not save backup {filename}: {str(e)}")
    
    def fetch_timeline_data(self) -> Optional[pd.DataFrame]:
        """Fetch historical measles timeline data"""
        df = self.fetch_with_fallback(
            primary_url=self.TIMELINE_API,
            alt_url=self.TIMELINE_API_ALT,
            backup_file='measles_timeline.csv',
            dataset_name='timeline'
        )
        
        if df is not None:
            df = self._process_timeline_data(df)
        
        return df
    
    def fetch_measles_data(self) -> Optional[pd.DataFrame]:
        """Fetch current measles cases data"""
        df = self.fetch_with_fallback(
            primary_url=self.MEASLES_API,
            alt_url=self.MEASLES_API_ALT,
            backup_file='measles_cases.csv',
            dataset_name='measles cases'
        )
        
        if df is not None:
            df = self._process_measles_data(df)
        
        return df
    
    def fetch_vaccination_data(self) -> Optional[pd.DataFrame]:
        """Fetch vaccination coverage data"""
        df = self.fetch_with_fallback(
            primary_url=self.VACCINATION_API,
            alt_url=self.VACCINATION_API,  # No alt endpoint for this one
            backup_file='vaccination_coverage.csv',
            dataset_name='vaccination coverage'
        )
        
        if df is not None:
            df = self._process_vaccination_data(df)
        
        return df
    
    def _process_timeline_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean timeline data"""
        try:
            # Ensure year column exists and is numeric
            year_col = 'year' if 'year' in df.columns else df.columns[0]
            df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
            
            # Ensure cases column exists and is numeric
            cases_col = 'cases' if 'cases' in df.columns else df.columns[1]
            df[cases_col] = pd.to_numeric(df[cases_col], errors='coerce')
            
            # Remove rows with missing data
            df = df.dropna(subset=[year_col, cases_col])
            
            # Sort by year
            df = df.sort_values(year_col)
            
            logging.info(f"Processed timeline data: {df[year_col].min():.0f} to {df[year_col].max():.0f}")
            
            return df
        except Exception as e:
            logging.error(f"Error processing timeline data: {str(e)}")
            return df
    
    def _process_measles_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean measles cases data with dynamic year handling"""
        try:
            # Identify column names (API may use different names)
            state_col = next((col for col in df.columns if 'state' in col.lower()), 'state')
            year_col = next((col for col in df.columns if 'year' in col.lower()), 'year')
            cases_col = next((col for col in df.columns if 'case' in col.lower()), 'cases')
            
            # Convert to appropriate types
            df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
            df[cases_col] = pd.to_numeric(df[cases_col], errors='coerce')
            
            # Remove rows with missing critical data
            df = df.dropna(subset=[state_col, year_col, cases_col])
            
            # Get most recent year's data
            most_recent_year = df[year_col].max()
            
            # Try to get current year data first
            current_year_data = df[df[year_col] == self.current_year].copy()
            
            if len(current_year_data) > 0:
                logging.info(f"Using current year ({self.current_year}) measles data: {len(current_year_data)} records")
                return current_year_data
            else:
                # Fall back to most recent available year
                logging.info(f"No {self.current_year} data available. Using most recent year: {most_recent_year:.0f}")
                recent_data = df[df[year_col] == most_recent_year].copy()
                return recent_data
                
        except Exception as e:
            logging.error(f"Error processing measles data: {str(e)}")
            return df
    
    def _process_vaccination_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Process and clean vaccination coverage data with dynamic year handling"""
        try:
            # Identify column names
            state_col = next((col for col in df.columns if 'state' in col.lower()), 'state')
            year_col = next((col for col in df.columns if 'year' in col.lower() or 'school_year' in col.lower()), 'year')
            coverage_col = next((col for col in df.columns if 'mmr' in col.lower() or 'coverage' in col.lower()), 'coverage')
            exemption_col = next((col for col in df.columns if 'exempt' in col.lower()), None)
            
            # Convert to appropriate types
            if year_col in df.columns:
                # Handle school year format like "2024-2025"
                if df[year_col].dtype == 'object' and '-' in str(df[year_col].iloc[0]):
                    df['year_numeric'] = df[year_col].str.split('-').str[0].astype(int)
                    year_col = 'year_numeric'
                else:
                    df[year_col] = pd.to_numeric(df[year_col], errors='coerce')
            
            df[coverage_col] = pd.to_numeric(df[coverage_col], errors='coerce')
            
            if exemption_col:
                df[exemption_col] = pd.to_numeric(df[exemption_col], errors='coerce')
            
            # Remove rows with missing critical data
            df = df.dropna(subset=[state_col, coverage_col])
            
            # Get most recent year's data
            if year_col in df.columns:
                most_recent_year = df[year_col].max()
                
                # Try current year or most recent
                current_data = df[df[year_col] >= self.current_year - 1].copy()  # Allow previous year for vaccination data
                
                if len(current_data) == 0:
                    current_data = df[df[year_col] == most_recent_year].copy()
                    logging.info(f"Using most recent vaccination data from {most_recent_year:.0f}")
                else:
                    logging.info(f"Using recent vaccination data: {len(current_data)} records")
                
                return current_data
            
            return df
            
        except Exception as e:
            logging.error(f"Error processing vaccination data: {str(e)}")
            return df
    
    def fetch_all_data(self) -> Dict[str, Optional[pd.DataFrame]]:
        """
        Fetch all required datasets
        
        Returns:
            Dictionary with dataset names as keys and DataFrames as values
        """
        logging.info("=" * 60)
        logging.info("Fetching all datasets...")
        logging.info("=" * 60)
        
        data = {
            'timeline': self.fetch_timeline_data(),
            'measles': self.fetch_measles_data(),
            'vaccination': self.fetch_vaccination_data()
        }
        
        # Log summary
        success_count = sum(1 for df in data.values() if df is not None)
        logging.info("=" * 60)
        logging.info(f"Data fetch complete: {success_count}/{len(data)} datasets successful")
        logging.info("=" * 60)
        
        return data
    
    def validate_data(self, data: Dict[str, Optional[pd.DataFrame]]) -> Dict[str, Dict]:
        """
        Validate fetched data
        
        Args:
            data: Dictionary of DataFrames to validate
            
        Returns:
            Dictionary with validation results for each dataset
        """
        results = {}
        
        for dataset_name, df in data.items():
            if df is None:
                results[dataset_name] = {
                    'valid': False,
                    'error': 'DataFrame is None',
                    'rows': 0
                }
            elif df.empty:
                results[dataset_name] = {
                    'valid': False,
                    'error': 'DataFrame is empty',
                    'rows': 0
                }
            elif len(df) < 10:  # Minimum threshold
                results[dataset_name] = {
                    'valid': False,
                    'error': f'Insufficient data: only {len(df)} rows',
                    'rows': len(df)
                }
            else:
                results[dataset_name] = {
                    'valid': True,
                    'rows': len(df),
                    'columns': list(df.columns)
                }
        
        return results
