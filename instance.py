import oci
import time
from dotenv import load_dotenv
import os
import sys

# Load environment variables from the .env file
load_dotenv()

# Configure OCI credentials
config = oci.config.from_file()

# Create a Compute client instance
compute_client = oci.core.ComputeClient(config)

# Check if the subnet_id variable is empty
subnet_id = os.getenv("subnet_id")
if not os.getenv("subnet_id"):
    print("Creating Network Components...")
    # Create a Networking client instance
    network_client = oci.core.VirtualNetworkClient(config)

    # Create a virtual cloud network (VCN)
    create_vcn_response = network_client.create_vcn(
        oci.core.models.CreateVcnDetails(
            cidr_block="10.0.0.0/16",
            compartment_id=config["tenancy"],
            display_name="VirtualCloudNetwork",
            dns_label="vnc"
        )
    )
    vcn_id = create_vcn_response.data.id

    # Create an Internet Gateway
    create_internet_gateway_response = network_client.create_internet_gateway(
        oci.core.models.CreateInternetGatewayDetails(
            compartment_id=config["tenancy"],
            vcn_id=vcn_id,
            display_name="InternetGateway",
            is_enabled=True
        )
    )
    internet_gateway_id = create_internet_gateway_response.data.id

    # Create a route table
    create_route_table_response = network_client.create_route_table(
        oci.core.models.CreateRouteTableDetails(
            compartment_id=config["tenancy"],
            vcn_id=vcn_id,
            display_name="RouteToInternetGateway",
            route_rules=[
                oci.core.models.RouteRule(
                    network_entity_id=internet_gateway_id,
                    destination="0.0.0.0/0"
                )
            ]
        )
    )
    route_table_id = create_route_table_response.data.id

    # Create a subnet in the newly created VCN
    create_subnet_response = network_client.create_subnet(
        oci.core.models.CreateSubnetDetails(
            compartment_id=config["tenancy"],
            display_name="Subnet",
            vcn_id=vcn_id,
            cidr_block="10.0.0.0/24",
            route_table_id=route_table_id,
            dns_label="subnet"
        )
    )
    subnet_id = create_subnet_response.data.id

    print("VCN created -> ID:", vcn_id)
    print("Subnet created -> ID:", subnet_id)
    print("Internet Gateway created -> ID:", internet_gateway_id)
    print("Route Table created -> ID:", route_table_id)

# Define the instance parameters
launch_instance_details = oci.core.models.LaunchInstanceDetails(
    compartment_id=config["tenancy"],
    availability_domain=os.getenv("availability_domain"),
    shape=os.getenv("shape"),
    display_name=os.getenv("instance_name"),
    create_vnic_details=oci.core.models.CreateVnicDetails(
        subnet_id=subnet_id
    ),
    availability_config=oci.core.models.LaunchInstanceAvailabilityConfigDetails(
        is_live_migration_preferred=True
    ),
    metadata={
        "ssh_authorized_keys": os.getenv("ssh_publickey"),
    },
    shape_config=oci.core.models.LaunchInstanceShapeConfigDetails(
        memory_in_gbs=float(os.getenv("memory")),
        ocpus=float(os.getenv("ocpus")),
    ),
    source_details=oci.core.models.InstanceSourceViaImageDetails(
        source_type="image",
        image_id=os.getenv("image_id"),
        boot_volume_size_in_gbs=int(os.getenv("boot_volume_gb")),
        boot_volume_vpus_per_gb=20,
    ),
)
try:
    while True:
        try:
            create_instance_response = compute_client.launch_instance(launch_instance_details)
            instance_id = create_instance_response.data.id
            print(f"Instance created with ID: {instance_id}")
            break  # Exit the loop if the instance is created successfully      
        except oci.exceptions.ServiceError as e:
            if e.code == "InternalError" and "Out of host capacity" in e.message:
                print("Error: No host capacity available. Waiting...")
                time.sleep(60)  # Wait for 1 minute before retrying
            else:
                raise e  # Raise any other exception
except KeyboardInterrupt:
    print("Program stopped by user.")
    sys.exit(0)