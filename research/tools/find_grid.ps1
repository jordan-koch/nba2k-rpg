$out = Join-Path $PSScriptRoot "..\..\out"
$path = $args[0]
$b = [System.IO.File]::ReadAllBytes($path)
Write-Output "file: $path  ($($b.Length) bytes)"

# Collect even-aligned UTF-16LE name-like strings: >=3 letters, terminated, ASCII-letter dominant
$offs = New-Object System.Collections.Generic.List[int]
$vals = New-Object System.Collections.Generic.List[string]
$i = 0
while ($i -lt $b.Length - 8) {
    $c = [BitConverter]::ToUInt16($b, $i)
    # must start with an uppercase letter
    if ($c -ge 65 -and $c -le 90) {
        $sb = New-Object System.Text.StringBuilder
        $j = $i
        $ok = $true
        while ($j -lt $b.Length - 2) {
            $ch = [BitConverter]::ToUInt16($b, $j)
            if ($ch -eq 0) { break }
            if (($ch -ge 65 -and $ch -le 90) -or ($ch -ge 97 -and $ch -le 122) -or $ch -eq 39 -or $ch -eq 45 -or $ch -eq 46 -or $ch -eq 32) {
                [void]$sb.Append([char]$ch); $j += 2
            } else { $ok = $false; break }
            if ($sb.Length -gt 30) { $ok = $false; break }
        }
        if ($ok -and $sb.Length -ge 3) {
            $offs.Add($i); $vals.Add($sb.ToString())
            $i = $j + 2
            continue
        }
    }
    $i += 2
}
Write-Output "utf16 name-like strings found: $($offs.Count)"

# Histogram of gaps between consecutive string offsets -> find dominant record stride
$gaps = @{}
for ($k = 1; $k -lt $offs.Count; $k++) {
    $d = $offs[$k] - $offs[$k-1]
    if ($d -gt 8 -and $d -lt 40000) { $gaps[$d] = 1 + [int]$gaps[$d] }
}
Write-Output ""
Write-Output "=== top 15 gaps between consecutive strings ==="
$gaps.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 15 | ForEach-Object { "  gap {0,-8} count {1}" -f $_.Key, $_.Value }

# Densest cluster: which 64KB window holds the most strings
Write-Output ""
Write-Output "=== densest 256KB windows ==="
$w = @{}
foreach ($o in $offs) { $k = [math]::Floor($o / 262144); $w[$k] = 1 + [int]$w[$k] }
$w.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 8 | ForEach-Object {
    "  window {0,-4} (byte {1,-12}) strings={2}" -f $_.Key, ($_.Key * 262144), $_.Value
}

# Show a sample from the densest window
$top = ($w.GetEnumerator() | Sort-Object Value -Descending | Select-Object -First 1).Key
$lo = $top * 262144; $hi = $lo + 262144
Write-Output ""
Write-Output "=== sample strings in densest window (byte $lo..$hi) ==="
$sample = for ($k = 0; $k -lt $offs.Count; $k++) {
    if ($offs[$k] -ge $lo -and $offs[$k] -lt $hi) {
        "  @{0,-10} {1}" -f $offs[$k], $vals[$k]
    }
}
$sample | Select-Object -First 50
