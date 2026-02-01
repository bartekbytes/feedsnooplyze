import argparse, sys
import time
from datetime import datetime


# import feedsnooplyze modules
from feedsnooplyze.parser import *
from feedsnooplyze.persistence import get_engine, persistence_setup, PersistenceCommand
from feedsnooplyze.configuration.config import ConfigLoader, ConfigReader
from feedsnooplyze.configuration.content_source_config import ContentSourceConfigReader, ContentSourceConfigLoader


def main():
    """
    Entry point for the feedsnooplyze application.
    Parses command-line arguments to determine the run mode ('setup' or 'fetch'),
    fetch type ('interactive' or 'oneshot'), pooling time, and configuration file path.
    Loads general, persistence, and notifications configuration from the specified config file.

    Runs the main logic of the application.
   
    Prints configuration details, setup status, and fetch progress to the console.
    """
    parser = argparse.ArgumentParser(
        description="📦 FeedSnooplyze",
        epilog="Example usage:\n  feedsnooplyze --run-mode [setup|fetch]\n --pooling-time [in seconds]\n --config-file [path to conf]",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("-r", "--run-mode", type=str, choices=["setup", "fetch"], required=True, help="Run mode of feedsnooplyze: setup or fetch")
    parser.add_argument("-ft", "--fetch-type", type=str, choices=["interactive", "oneshot"], required=False, help="Fetch type: interactive in console, oneshot run from external orchestrator")
    parser.add_argument("-p", "--pooling-time", type=int, help="When fetch-type is interactive, how often to pool data")
    parser.add_argument("-f", "--config-file", type=str, help="Path to configuration file")
    
    if len(sys.argv) == 1:
        parser.print_help(sys.stderr)
        sys.exit(1)

    args = parser.parse_args()

    # Check arguments consistency
    if args.run_mode == 'fetch' and args.config_file is None:
        parser.error("When run-mode is 'fetch', config-file must be provided")
    
    if args.run_mode == 'fetch' and args.fetch_type is None:
        parser.error("When run-mode is 'fetch', fetch-type must be provided")

    # Read app config file
    cr = ConfigReader(r"config.yaml") # expecting a config file here with this name
    cl = ConfigLoader(reader=cr)
    general_config, persistence_config, notifications_config = cl.load_config() # Get all 3 types of Config: general, persistence and notifications

    print("⚙️ Config loaded:")
    print(f"General Config: {general_config}")
    print(f"Persistence Config: {persistence_config}")
    print(f"Notifications Config:")
    for n in notifications_config:
        print(n)

    if args.run_mode == 'setup':
        
        print("🔧 Running setup...")

        persistence_engine = get_engine(persistence_config)

        persistence_setup_result = persistence_setup(persistence_engine, persistence_config)
        if persistence_setup_result:
            print("✅ Persistence Layer setup completed successfully!")
        else:
            print("❌ Persistence Layer setup failed!")
            exit(-1)

    elif args.run_mode == 'fetch':
            
        # Read Pages config file
        cscr = ContentSourceConfigReader(args.config_file)
        cscl = ContentSourceConfigLoader(reader=cscr)
        monitors = cscl.load_config() # parse and load config, return ContentSourceConfig instance
        
        pages_monitors = monitors.pages_config # extract list of PageMonitor from ContentSourceConfig instance
        rss_monitors = monitors.rsses_config # extract list of RSSMonitor from ContentSourceConfig instance

        print(f"pages_monitors loaded: {pages_monitors}")
        print(f"rss_monitors loaded: {rss_monitors}")

        # Create and Connect to Persistence Engine
        persistence_engine = get_engine(persistence_config)
        print(persistence_engine)

        if not persistence_engine:
            print("❌ Can't connect to Persistence Engine!")
            exit(1)

        
        #############################
        # Main logic of the app
        #############################
        
        loop_counter: int = 1
        pooling_time = None
        
        # If running mode is 'interactive' then pooling_time must be setup.
        # pooling_time from command-line arguments takes precedence over pooling_time from the configuration file.
        if args.fetch_type == 'interactive':
            pooling_time = args.pooling_time if args.pooling_time else general_config.pooling_time
            print(f"Pooling time set to: {pooling_time}")

        # Mode how app works, interactive or oneshot
        if args.fetch_type == 'interactive' or args.fetch_type == 'oneshot':
            

            persistence_command = PersistenceCommand(persistence_engine)

            while True:
                
                # Get date and time as of now and format it to a human-readable string
                now = datetime.now()
                formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")

                print("\n------------------")
                print(f"- 📥 Fetching data ({args.fetch_type} mode) at {formatted_time} (Loop counter: {loop_counter})...")
                print("------------------\n")

                # For now, just show the content of each RSS feed
                # Full logic to be implemented later
                for rssm in rss_monitors:
                    rssm.notifiers = notifications_config
                    rssm.get_rss()

                # For each of PageMonitor instance inside pages_monitors list...
                for pm in pages_monitors:

                    pm.notifiers = notifications_config
                
                    # 1. Check if there is already any PageContent available in Persistence Layer for a given Page
                    content_available = persistence_command.is_content_available(page_name=pm.page.name)

                    if content_available:

                        # Get the latest PageContent (ordered by ContentTime) for a given Page
                        page_content = persistence_command.get_latest_by_name(page_name=pm.page.name)

                        # 2. Check if there is any content change since the last saved content
                        pc = pm.check_for_content_update(latest_persisted_hash=page_content.content_hash, latest_persisted_content=page_content.full_content)
                    
                        # If a new content detected, add it to the Persisitence Layer
                        if pc.page_name:
                    
                            # 3. Add new content to Persistence
                            persistence_command.add_content(page_name=pc.page_name, content_time=pc.content_time, 
                                                         content_hash=pc.content_hash, full_content=pc.full_content, added_content=pc.added_content)
                
                    else:
                        # There is no content stored in Persistence Layer for a given Page,
                        # so execute check for content update with dummy hash and content
                        pc = pm.check_for_content_update(latest_persisted_hash=None, latest_persisted_content=None)
                        persistence_command.add_content(page_name=pc.page_name, content_time=pc.content_time,
                                                     content_hash=pc.content_hash, full_content=pc.full_content, added_content=pc.added_content)
                

                # Infinite loop for 'interactive' mode.
                # For 'oneshot' mode, break the loop after the first run.
                if args.fetch_type == 'oneshot':
                    break
                else:
                    loop_counter = loop_counter + 1
                    time.sleep(pooling_time)
                
        else:
            print("❌ Can't execute fetching data")



if __name__ == "__main__":
    main()
