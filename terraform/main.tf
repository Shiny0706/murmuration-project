terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0.1"
    }
  }
}

provider "docker" {}

resource "docker_network" "app_network" {
  name = "app_network"
}

resource "docker_image" "backend" {
  name = "backend"
  build {
    context = "../backend"
  }
}

resource "docker_image" "frontend" {
  name = "frontend"
  build {
    context = "../frontend"
  }
}

resource "docker_container" "backend" {
  name  = "backend"
  image = docker_image.backend.latest
  ports {
    internal = 8000
    external = 8000
  }
  networks_advanced {
    name = docker_network.app_network.name
  }
}

resource "docker_container" "frontend" {
  name  = "frontend"
  image = docker_image.frontend.latest
  ports {
    internal = 3000
    external = 3000
  }
  networks_advanced {
    name = docker_network.app_network.name
  }
  depends_on = [docker_container.backend]
} 