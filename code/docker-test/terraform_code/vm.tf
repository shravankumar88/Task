variable "prefix" {
  default = "webapp"
}

resource "azurerm_resource_group" "main" {
  name     = "${var.prefix}-resources"
  location = "West US 2"
}

resource "azurerm_virtual_network" "main" {
  name                = "${var.prefix}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
}
resource "azurerm_public_ip" "main-public-ip" {
  location                     = "West US 2"
  name                         = "webapp-ip"
  resource_group_name          = "azurerm_resource_group.main.name"
  public_ip_address_allocation = "static"
}

resource "azurerm_subnet" "internal" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.main.name
  virtual_network_name = azurerm_virtual_network.main.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_network_interface" "main" {
  name                = "${var.prefix}-nic"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name

  ip_configuration {
    name                          = "testconfiguration1"
    subnet_id                     = azurerm_subnet.internal.id
    private_ip_address_allocation = "Dynamic"
    public_ip_address_id          = "${azurerm_public_ip.main-public-ip.id}"
  }
}

resource "azurerm_virtual_machine" "main" {
  name                  = "${var.prefix}-vm"
  location              = azurerm_resource_group.main.location
  resource_group_name   = azurerm_resource_group.main.name
  network_interface_ids = [azurerm_network_interface.main.id]
  vm_size               = "Standard_DS1_v2"

   delete_os_disk_on_termination = true

   delete_data_disks_on_termination = true

  storage_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "16.04-LTS"
    version   = "latest"
  }
  storage_os_disk {
    name              = "myosdisk1"
    caching           = "ReadWrite"
    create_option     = "FromImage"
    managed_disk_type = "Standard_LRS"
  }
  os_profile {
    computer_name  = "webapp01"
    admin_username = "ubuntu"
  }
os_profile_linux_config {
    disable_password_authentication = true

    ssh_keys {
      key_data = "${file(var.authorized-keys)}"
      # This is required for some reason, but must be always like that. The
      # only thing that may change is the username.
      # https://www.terraform.io/docs/providers/azurerm/r/virtual_machine.html
      path = "/home/ubuntu/.ssh/authorized_keys"
    }
  }

  tags = {
    environment = "staging"
  }

}
resource "null_resource" "webapp_provisioner" {
  triggers = {
    webapp_vm_id = "${azurerm_virtual_machine.main.id}"
  }
  connection {
    host = "${azurerm_public_ip.main-public-ip.ip_address}"
    user = "ubuntu"
    private_key = "${file(var.ssh-keys)}"
  }

  provisioner "remote-exec" {

    inline = [
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"",
      "sudo apt-get update",
      "sudo apt-cache policy docker-ce",
      "sudo apt-get install -y docker-ce",
      "sudo systemctl status docker",
      "sudo usermod -aG docker ubuntu",
    ]
  }

}
