class Package:
    def __init__(self, package_id, weight, destination):
        self.package_id = package_id
        self.weight = weight
        self.destination = destination

    def __str__(self):
        return f"{self.package_id} | {self.weight} | {self.destination}" 
