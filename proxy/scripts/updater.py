import requests, os, hashlib

print("Checking for updates...")

# get latest version
project = requests.get("https://api.papermc.io/v2/projects/velocity/").json()
latest = project["versions"][-1]
builds = requests.get(f"https://api.papermc.io/v2/projects/velocity/versions/{latest}/builds").json()
latest_build = builds["builds"][-1]

# check if latest version is already downloaded
current_hash = ""
try:
    with open("../velocity.jar", "rb", buffering=0) as f:
        h = hashlib.sha256()
        b = bytearray(128*1024)
        m = memoryview(b)
        while n := f.readinto(m):
            h.update(m[:n])
        current_hash = h.hexdigest()
    if current_hash == latest_build["downloads"]["application"]["sha256"]:
        print(f"Latest Velocity version already downloaded")
        exit()
    else:
        print(f"New version available! ({latest} #{latest_build['build']})")
        # delete old version
        os.remove("velocity.jar")
except FileNotFoundError:
    pass

# download latest version
print(f"Downloading Velocity {latest} #{latest_build['build']}...")
r = requests.get(f"https://api.papermc.io/v2/projects/velocity/versions/{latest}/builds/{latest_build['build']}/downloads/{latest_build['downloads']['application']['name']}")
with open("../velocity.jar", "wb") as f:
    f.write(r.content)
    
# verify download
print("Verifying download...")
with open("../velocity.jar", "rb", buffering=0) as f:
    h = hashlib.sha256()
    b = bytearray(128*1024)
    m = memoryview(b)
    while n := f.readinto(m):
        h.update(m[:n])
    if h.hexdigest() != latest_build["downloads"]["application"]["sha256"]:
        print("Download verification failed! Please manually re-run this script or download a copy of Velocity from https://papermc.io/downloads/velocity.")
        exit()
    else:
        print("Download verified!")

print("Done!")
