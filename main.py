import psutil
import argparse
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("monitor_services.log"),
        logging.StreamHandler(sys.stdout)
    ]
)

def setup_argparse():
    """
    Set up command line argument parsing.
    """
    parser = argparse.ArgumentParser(
        description="Monitor critical service status and provide alerts."
    )
    parser.add_argument(
        '--services',
        type=str,
        nargs='+',
        required=True,
        help="List of services to monitor, separated by spaces."
    )
    return parser.parse_args()

def monitor_services(service_names):
    """
    Monitor the status of the specified services.

    Args:
        service_names (list): List of service names to monitor.
    """
    try:
        for service_name in service_names:
            service_found = False
            for service in psutil.win_service_iter():
                if service.name().lower() == service_name.lower():
                    service_found = True
                    service_status = service.status()
                    logging.info(f"Service '{service_name}' is {service_status}.")
                    if service_status != "running":
                        logging.warning(f"Service '{service_name}' is not running!")
                    break
            if not service_found:
                logging.error(f"Service '{service_name}' not found.")
    except Exception as e:
        logging.error(f"An error occurred while monitoring services: {e}")

def main():
    """
    Main function to execute the service monitoring tool.
    """
    try:
        args = setup_argparse()
        monitor_services(args.services)
    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()