set +o xtrace

. $DEST/phoenix/devstack/lib/phoenix

# check for service enabled
if is_service_enabled phoenix-ai phoenix-api; then
    if [[ "$1" == "stack" && "$2" == "pre-install" ]]; then
        # Set up system services
        echo_summary "Configuring system services phoenix"

    elif [[ "$1" == "stack" && "$2" == "install" ]]; then
        # Perform installation of service source
        echo_summary "Installing phoenix"
        install_phoenix

    elif [[ "$1" == "stack" && "$2" == "post-config" ]]; then
        # Configure after the other layer 1 and 2 services have been configured
        echo_summary "Configuring phoenix"
        configure_phoenix

    elif [[ "$1" == "stack" && "$2" == "extra" ]]; then
        # Initialize and start the phoenix service
        init_phoenix
        echo_summary "Initializing phoenix"
        start_phoenix
    fi

    if [[ "$1" == "unstack" ]]; then
        # Shut down phoenix services
        stop_phoenix
    fi

    if [[ "$1" == "clean" ]]; then
        # Remove state and transient data
        # Remember clean.sh first calls unstack.sh
        # no-op
        cleanup_phoenix
    fi
fi