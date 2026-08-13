$scratch = Join-Path $PSScriptRoot "..\..\out"
if (-not (Test-Path $scratch)) { New-Item -ItemType Directory -Force $scratch | Out-Null }
$path    = $args[0]
$STRIDE  = 17234
$b = [System.IO.File]::ReadAllBytes($path)
Write-Output "file: $(Split-Path $path -Leaf)  ($($b.Length) bytes)  stride=$STRIDE"

function ReadU16($buf, $off, $maxChars = 28) {
    if ($off -lt 0 -or $off + 2 -ge $buf.Length) { return $null }
    $sb = New-Object System.Text.StringBuilder
    for ($i = 0; $i -lt $maxChars; $i++) {
        $p = $off + $i * 2
        if ($p + 1 -ge $buf.Length) { break }
        $c = [BitConverter]::ToUInt16($buf, $p)
        if ($c -eq 0) { break }
        if ($c -lt 32 -or $c -gt 0x17F) { return $null }
        [void]$sb.Append([char]$c)
    }
    if ($sb.Length -lt 2) { return $null }
    return $sb.ToString()
}

# Phase-lock: score every residue class mod STRIDE by how many slots yield last+first names
$best = $null
# sample candidate starts from actual string positions to keep it cheap
$cands = New-Object System.Collections.Generic.HashSet[int]
$i = 0
while ($i -lt $b.Length - 8) {
    $c = [BitConverter]::ToUInt16($b, $i)
    if ($c -ge 65 -and $c -le 90) {
        $l = ReadU16 $b $i
        $f = ReadU16 $b ($i + 40)
        if ($l -and $f) { [void]$cands.Add($i % $STRIDE) }
    }
    $i += 2
}
Write-Output "candidate phases: $($cands.Count)"

foreach ($ph in $cands) {
    $n = 0
    for ($o = $ph; $o + $STRIDE -lt $b.Length; $o += $STRIDE) {
        if ((ReadU16 $b $o) -and (ReadU16 $b ($o + 40))) { $n++ }
    }
    if (-not $best -or $n -gt $best.N) { $best = @{ Phase = $ph; N = $n } }
}
Write-Output "best phase = $($best.Phase)  with $($best.N) populated records"
Write-Output ""

$players = @()
for ($o = $best.Phase; $o + $STRIDE -lt $b.Length; $o += $STRIDE) {
    $last = ReadU16 $b $o; $first = ReadU16 $b ($o + 40)
    if ($last -and $first) { $players += [PSCustomObject]@{ Offset=$o; First=$first; Last=$last } }
}
Write-Output "TOTAL PLAYERS: $($players.Count)"
Write-Output ""
Write-Output "--- first 45 ---"
$players | Select-Object -First 45 | ForEach-Object { "  {0,-14} {1,-18} @{2}" -f $_.First, $_.Last, $_.Offset }
Write-Output ""
Write-Output "--- random 20 ---"
$players | Select-Object -Skip ([int]($players.Count/2)) -First 20 | ForEach-Object { "  {0,-14} {1,-18} @{2}" -f $_.First, $_.Last, $_.Offset }

$players | Export-Csv "$scratch\grid_players.csv" -NoTypeInformation -Encoding UTF8
Write-Output ""
Write-Output "wrote $scratch\grid_players.csv"

# Hexdump the first 320 bytes of one well-known record for structure inspection
$star = $players | Where-Object { $_.Last -in @('Curry','James','Jokic','Doncic','Tatum') } | Select-Object -First 1
if ($star) {
    Write-Output ""
    Write-Output "=== record layout: $($star.First) $($star.Last) @ $($star.Offset) ==="
    for ($r = 0; $r -lt 320; $r += 16) {
        $p = $star.Offset + $r
        if ($p + 16 -ge $b.Length) { break }
        $sl = $b[$p..($p+15)]
        $hex = ($sl | ForEach-Object { $_.ToString('X2') }) -join ' '
        $asc = -join ($sl | ForEach-Object { if ($_ -ge 32 -and $_ -lt 127) { [char]$_ } else { '.' } })
        "  +{0,-5} {1}  {2}" -f $r, $hex, $asc
    }
}
