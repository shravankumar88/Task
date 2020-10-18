resource "azure_storage_blob" "image" {
  name                   = "image-blob"
  storage_service_name   = "image"
  storage_container_name = "image-storage-container"
  type                   = "BlockBlob"
}
