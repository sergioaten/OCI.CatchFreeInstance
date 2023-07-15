# Resolving the Oracle Cloud "Out of Capacity" Problem and Acquiring a Free VPS with 4 ARM Cores / 24GB of Memory

This Python script creates a virtual machine instance in Oracle Cloud Infrastructure (OCI) using the OCI Python SDK. If there is available host capacity, the script attempts to create the instance. It also sets up the necessary networking components if the subnet ID is not provided as an environment variable.

## Prerequisites

Before running the script, ensure you have met the following requirements:

- Python 3.x installed
- The OCI Python SDK installed (`oci` package)
- An OCI account with the necessary permissions to create resources (virtual machine, VCN, subnet, etc.)
- An OCI configuration file (`config`) with valid credentials

## Installation

1. Clone the repository or download the script file to your local machine.
    ```
    git clone https://github.com/sergioaten/OCI.catch-free-instance.git
    ```

2. Install the required dependencies by running the following command:

   ```
   pip install -r requierements.txt
   ```

3. Set up your OCI configuration by following the instructions in the [OCI SDK and CLI Configuration](https://docs.oracle.com/en-us/iaas/Content/API/Concepts/sdkconfig.htm) documentation.

4. Create a `.env` file in the same directory as the script and provide the required environment variables:

   - `subnet_id`: (Optional) The OCID of the subnet where the instance will be launched. If not provided, the script will create a new VCN, subnet, and associated networking components.
   - `availability_domain`: The availability domain where the instance will be launched.
   - `shape`: The shape (compute instance type) for the instance.
   - `instance_name`: The display name for the instance.
   - `ssh_publickey`: The public SSH key to be added to the instance for SSH access.
   - `memory`: The amount of memory (in GB) for the instance.
   - `ocpus`: The number of OCPUs for the instance.
   - `image_id`: The OCID of the image to be used for the instance.
   - `boot_volume_gb`: The size (in GB) of the boot volume for the instance.

## Usage

Run the script using the following command:

```
python instance.py
```

The script will perform the following steps:

1. Load the environment variables from the `.env` file.

2. Configure the OCI credentials using the `config` file.

3. Create an OCI Compute client instance.

4. Check if the `subnet_id` variable is empty. If empty, the script proceeds to create the necessary networking components (VCN, subnet, internet gateway, and route table).

5. Define the instance parameters based on the provided environment variables.

6. Attempt to launch the instance. If an "Out of host capacity" error occurs, the script waits for 1 minute before retrying. This is to handle cases where there is no available host capacity.

7. Once the instance is successfully created, the script displays the instance ID.

## Contributing

Contributions to this script are welcome. If you find any issues or have suggestions for improvements, please open an issue or submit a pull request on the GitHub repository.

## License

This script is licensed under the [MIT License](https://opensource.org/licenses/MIT). See the `LICENSE` file for more information.
