# NBA 2K26 IFF toolkit: manifest lookup -> blob slice -> Oodle Kraken -> ZIP entries
$GAME    = "D:\Programs\Steam\steamapps\common\NBA 2K26"
$OUT     = Join-Path $PSScriptRoot "..\..\out"
if (-not (Test-Path $OUT)) { New-Item -ItemType Directory -Force $OUT | Out-Null }
$DLL     = "$GAME\data\oodle\oo2core_9_win64.dll"

if (-not ("Oodle" -as [type])) {
Add-Type -TypeDefinition @"
using System;
using System.Runtime.InteropServices;
public static class Oodle {
    [DllImport(@"D:\Programs\Steam\steamapps\common\NBA 2K26\data\oodle\oo2core_9_win64.dll", CallingConvention=CallingConvention.Cdecl)]
    public static extern IntPtr OodleLZ_Decompress(
        byte[] compBuf, IntPtr compBufSize, byte[] rawBuf, IntPtr rawLen,
        int fuzzSafe, int checkCRC, int verbosity,
        IntPtr decBufBase, IntPtr decBufSize, IntPtr fpCallback, IntPtr callbackUserData,
        IntPtr decoderMemory, IntPtr decoderMemorySize, int threadPhase);
}
"@
}

function Get-IffManifest {
    if (-not $script:MANIFEST) {
        $script:MANIFEST = @{}
        foreach ($line in [System.IO.File]::ReadLines("$GAME\manifest")) {
            $p = $line.Split(',')
            if ($p.Length -ge 4) { $script:MANIFEST[$p[0]] = @{ Blob=$p[1]; Off=[int64]$p[2]; Len=[int]$p[3] } }
        }
    }
    return $script:MANIFEST
}

# Read the raw (still IFF-framed) bytes for a manifest entry
function Get-IffBytes([string]$name) {
    $m = (Get-IffManifest)[$name]
    if (-not $m) { throw "not in manifest: $name" }
    $fs = [System.IO.File]::OpenRead("$GAME\$($m.Blob)")
    try {
        $fs.Seek($m.Off, 'Begin') | Out-Null
        $buf = New-Object byte[] $m.Len
        $got = 0
        while ($got -lt $m.Len) { $n = $fs.Read($buf, $got, $m.Len - $got); if ($n -le 0) { break }; $got += $n }
    } finally { $fs.Close() }
    return $buf
}

# IFF -> decompressed ZIP bytes
function Expand-Iff([byte[]]$iff) {
    if ($iff.Length -lt 32 -or $iff[0] -ne 0x1F -or $iff[1] -ne 0x8B) { throw "not an IFF (bad magic)" }
    $rawSize = [BitConverter]::ToUInt32($iff, $iff.Length - 4)
    if ($rawSize -le 0 -or $rawSize -gt 600MB) { throw "implausible raw size $rawSize" }
    $comp = New-Object byte[] ($iff.Length - 16)
    [Array]::Copy($iff, 16, $comp, 0, $comp.Length)
    $raw = New-Object byte[] $rawSize
    $r = [int64][Oodle]::OodleLZ_Decompress($comp, [IntPtr]$comp.Length, $raw, [IntPtr]$rawSize,
            1,0,0,[IntPtr]::Zero,[IntPtr]::Zero,[IntPtr]::Zero,[IntPtr]::Zero,[IntPtr]::Zero,[IntPtr]::Zero,3)
    if ($r -le 0) { throw "Oodle failed ($r)" }
    return $raw
}

# List entries inside an IFF by manifest name
function Get-IffEntries([string]$name) {
    $zipBytes = Expand-Iff (Get-IffBytes $name)
    $ms = New-Object System.IO.MemoryStream (,$zipBytes)
    $z  = New-Object System.IO.Compression.ZipArchive($ms, [System.IO.Compression.ZipArchiveMode]::Read)
    $out = $z.Entries | ForEach-Object { [PSCustomObject]@{ Iff=$name; Entry=$_.FullName; Size=$_.Length } }
    $z.Dispose(); $ms.Dispose()
    return $out
}

# Pull a single entry's bytes out of an IFF
function Get-IffEntryBytes([string]$name, [string]$entry) {
    $zipBytes = Expand-Iff (Get-IffBytes $name)
    $ms = New-Object System.IO.MemoryStream (,$zipBytes)
    $z  = New-Object System.IO.Compression.ZipArchive($ms, [System.IO.Compression.ZipArchiveMode]::Read)
    $e  = $z.Entries | Where-Object { $_.FullName -eq $entry } | Select-Object -First 1
    if (-not $e) { $z.Dispose(); $ms.Dispose(); throw "no entry $entry in $name" }
    $s = $e.Open(); $o = New-Object System.IO.MemoryStream; $s.CopyTo($o); $s.Close()
    $bytes = $o.ToArray(); $z.Dispose(); $ms.Dispose()
    return $bytes
}

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
