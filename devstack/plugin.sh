set +o xtrace

. $DEST/cow/devstack/lib/cow

# check for service enabled
if is_service_enabled cow-ai cow-api cow-agent-notification; then
    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services Cow"

    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of service source
        echo_summary "Installing cow"
        install_cow

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configuring cow"
        configure_cow

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize and start the cow service
        init_cow
        echo_summary "Initializing cow"
        start_cow
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down cow services
        stop_cow
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        cleanup_cow
    fi
fi