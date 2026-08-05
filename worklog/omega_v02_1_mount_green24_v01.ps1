$ErrorActionPreference = 'Stop'
$keyPath = 'C:\Users\maxre\Nextcloud\zSyncMain\ssh\asto_bitwarden_ed25519_20260618.txt'
if ([string]::IsNullOrWhiteSpace($env:TAYGETA_ADMIN_PASSWORD)) {
    throw 'Taygeta administrator password was not supplied by the credential helper.'
}
$env:TAYGETA_ADMIN_PASSWORD | ssh -o BatchMode=yes -i $keyPath rempel@astolfodebian.tail251d88.ts.net "ssh -o BatchMode=yes -i ~/.ssh/sol_key maxre@192.168.1.142 'sudo -S -p "" systemctl start mnt-green24.mount'"
if ($LASTEXITCODE -ne 0) {
    throw "Green24 mount command failed with exit code $LASTEXITCODE."
}
