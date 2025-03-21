provider "google" {
  project = "western-notch-453423-p9"
  region = "us-central1"
}

resource "google_container_cluster" "assignment-cluster" {
  name = "assignment-cluster"
  location = "us-central1"
  remove_default_node_pool = true
  initial_node_count = 1
}

resource "google_container_node_pool" "node-pool" {
  name = "node-pool"
  cluster = google_container_cluster.assignment-cluster.name
  location = google_container_cluster.assignment-cluster.location
  node_count = 1

  node_config {
    machine_type = "e2-micro"
    disk_size_gb = 10
    disk_type = "pd-standard"
    image_type = "COS_CONTAINERD"
  }
}

resource "null_resource" "get_credentials" {
  depends_on = [google_container_cluster.assignment-cluster]
  provisioner "local-exec" {
    command = "gcloud container clusters get-credentials assignment-cluster --location=us-central1"
  }
}

resource "null_resource" "kubectl_apply" {
  depends_on = [null_resource.get_credentials]
  provisioner "local-exec" {
    command = "kubectl apply -f deployment.yaml"
    working_dir = path.module
  }
}
