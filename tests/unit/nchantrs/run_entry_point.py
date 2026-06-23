#!/usr/bin/env python3
"""
nchantrs Entry Point Runner

Usage:
    python run_entry_point.py aberration   # L1 - Single widget dialog
    python run_entry_point.py distortion   # L2 - Complex dialog
    python run_entry_point.py nchantment   # L3 - Full application
    python run_entry_point.py --help       # Show this help
"""

import sys
import os
import logging
import argparse

# Set Qt platform BEFORE any Qt imports
os.environ['QT_QPA_PLATFORM'] = 'offscreen'

# Add project to path
sys.path.insert(0, '/home/solubrew/.arthr/workspace/projects/nchantrs')

# Configure logging - output to both terminal and log file
LOG_DIR = '/home/solubrew/.senbai/workspace'
LOG_FILE = os.path.join(LOG_DIR, 'nchantrs_entry_point.log')

# Create logger
logger = logging.getLogger('nchantrs_entry_point')
logger.setLevel(logging.DEBUG)

# Create formatters
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# File handler - logs to file
file_handler = logging.FileHandler(LOG_FILE)
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

# Console handler - logs to terminal
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Redirect print statements to logger
class PrintLogger:
    def write(self, message):
        if message.strip():
            logger.info(message.strip())
    
    def flush(self):
        pass

sys.stdout = PrintLogger()
sys.stderr = PrintLogger()


def run_aberration():
    """L1: Single widget dialog"""
    logger.info("Running aberration (L1 - Single widget dialog)...")
    from nchantrs.nchantrs import aberration
    
    # Use full module path for widget - this is what loadWidget expects
    widget = 'nchantrs.widgets.annotations.NchantdLabel'
    cfg = {
        'name': 'Test Label',
        'widget': widget,
    }
    
    aberration(name='Test Label', widget=widget, cfg=cfg)


def run_distortion():
    """L2: Complex dialog with multiple widgets"""
    logger.info("Running distortion (L2 - Complex dialog)...")
    from nchantrs.nchantrs import distortion
    
    # Use full module path for widget
    widget = 'nchantrs.widgets.annotations.NchantdLabel'
    cfg = {
        'name': 'Test App',
        'widget': widget,
        'theme': 'dark',
    }
    
    distortion(name='Test App', args={}, widget=widget, cfg=cfg)


def run_nchantment():
    """L3: Full application"""
    import os
    
    logger.info("Running nchantment (L3 - Full application)...")
    
    # Use offscreen Qt platform for headless operation
    os.environ['QT_QPA_PLATFORM'] = 'offscreen'
    
    from nchantrs.nchantrs import nchantment
    
    # Full application with profile
    profile = 'default'
    
    nchantment(name='Nchantment', args={}, profile_override=profile)


def main():
    parser = argparse.ArgumentParser(
        description='nchantrs Entry Point Runner',
        epilog='Examples:\n  python run_entry_point.py aberration\n  python run_entry_point.py distortion\n  python run_entry_point.py nchantment'
    )
    
    parser.add_argument(
        'entry_point',
        choices=['aberration', 'distortion', 'nchantment'],
        help='Entry point level to run (L1-L3)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.info(f"Starting {args.entry_point}...")
    
    # Run the selected entry point
    if args.entry_point == 'aberration':
        run_aberration()
    elif args.entry_point == 'distortion':
        run_distortion()
    elif args.entry_point == 'nchantment':
        run_nchantment()


if __name__ == '__main__':
    main()
