import nfl_data_py as nfl
from prettytable import PrettyTable
import time
import os
from datetime import datetime

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_current_week_games():
    """Get games for the current week"""
    try:
        # Get current year
        current_year = datetime.now().year
        
        # Load current season schedule
        schedule = nfl.import_schedules([current_year])
        
        # Filter for games that have started or finished (have scores)
        # Also include games that are scheduled for today
        current_games = schedule[
            (schedule['home_score'].notna()) | 
            (schedule['away_score'].notna()) |
            (schedule['gameday'] == datetime.now().strftime('%Y-%m-%d'))
        ].copy()
        
        # Sort by game date and time
        current_games = current_games.sort_values(['gameday', 'gametime']).reset_index(drop=True)
        
        return current_games
        
    except Exception as e:
        print(f"Error fetching NFL data: {e}")
        return None

def create_scores_table(games_df):
    """Create a formatted table of NFL scores"""
    if games_df is None or games_df.empty:
        return "No games data available"
    
    # Create the table
    table = PrettyTable()
    table.field_names = ["Week", "Home Team", "Away Team", "Home Score", "Away Score", "Status"]
    
    # Configure table appearance
    table.align = "c"  # Center align all columns
    table.padding_width = 1
    
    for _, game in games_df.iterrows():
        week = game.get('week', 'N/A')
        home_team = game.get('home_team', 'N/A')
        away_team = game.get('away_team', 'N/A')
        home_score = game.get('home_score', '-')
        away_score = game.get('away_score', '-')
        
        # Determine game status
        if home_score == '-' or away_score == '-' or str(home_score) == 'nan' or str(away_score) == 'nan':
            status = "Scheduled"
            home_score = "-"
            away_score = "-"
        else:
            home_score = int(float(home_score)) if str(home_score) != 'nan' else '-'
            away_score = int(float(away_score)) if str(away_score) != 'nan' else '-'
            status = "Final"
        
        table.add_row([week, home_team, away_team, home_score, away_score, status])
    
    return str(table)

def display_live_scores():
    """Main function to display and update NFL scores"""
    print("NFL Live Scores Tracker")
    print("Press Ctrl+C to exit")
    print("=" * 50)
    
    try:
        while True:
            clear_screen()
            
            # Display header with current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"NFL LIVE SCORES - Last Updated: {current_time}")
            print("=" * 70)
            
            # Get and display current games
            games = get_current_week_games()
            scores_table = create_scores_table(games)
            print(scores_table)
            
            print("\nUpdating every 60 seconds... (Press Ctrl+C to exit)")
            
            # Wait 60 seconds before next update
            time.sleep(60)
            
    except KeyboardInterrupt:
        print("\nExiting NFL Live Scores Tracker...")
    except Exception as e:
        print(f"An error occurred: {e}")

def show_sample_table():
    """Show a sample table with mock data"""
    table = PrettyTable()
    table.field_names = ["Week", "Home Team", "Away Team", "Home Score", "Away Score", "Status"]
    table.align = "c"
    
    # Sample data
    sample_games = [
        [3, "BUF", "MIA", 24, 17, "Final"],
        [3, "KC", "PHI", 28, 21, "Final"],
        [3, "SF", "LAR", 31, 14, "Final"],
        [3, "DAL", "NYG", "-", "-", "Scheduled"],
        [3, "BAL", "PIT", 20, 23, "Final"]
    ]
    
    for game in sample_games:
        table.add_row(game)
    
    return str(table)

if __name__ == "__main__":
    # Show sample first, then start live tracking
    print("Sample NFL Scores Table:")
    print(show_sample_table())
    print("\nStarting live scores tracker in 5 seconds...")
    time.sleep(5)
    
    display_live_scores()