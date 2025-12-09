"""
Task scheduler using schedule library
"""
import schedule
import time
from datetime import datetime

from .autoclose_overdue import auto_close_overdue_tasks


def run_scheduler(interval_minutes: int = 15):
    """
    Run scheduled task auto-closing
    
    Args:
        interval_minutes: Interval in minutes between checks
    """
    print(f"🚀 Starting task scheduler (checking every {interval_minutes} minutes)")
    print(f"Started at: {datetime.now()}")
    
    # Schedule the auto-close task
    schedule.every(interval_minutes).minutes.do(
        lambda: auto_close_overdue_tasks(dry_run=False)
    )
    
    # Run immediately once
    print("\n🔍 Running initial check...")
    auto_close_overdue_tasks(dry_run=False)
    
    # Keep running
    try:
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    except KeyboardInterrupt:
        print("\n\n🛑 Scheduler stopped by user")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run scheduled tasks")
    parser.add_argument("--interval", type=int, default=15, 
                       help="Interval in minutes (default: 15)")
    
    args = parser.parse_args()
    run_scheduler(args.interval)