<#=====AP========================================================||>
    Given a JSON file, Calculate edge time distance vectors
<#===============================================================||#>

$DB   = @()
$JSON = [IO.File]::ReadAllLines("$pwd/redirecting.json") | ConvertFrom-Json
function Get-Resource($route) {if (test-path -type leaf "$pwd/Live-Data/2015-02-04_19_05/${route}-bus") {[IO.File]::ReadAllLines("$pwd/Live-Data/2015-02-04_19_05/${route}-bus") | ConvertFrom-Json}}
function Diffr($times,$ind) {
    if (!$times[$ind-1].predictions) {return "NA"}
    Write-AP ">*Recieved Time: $(Print-List $times[$ind-1].predictions.seconds)"
    $src = $times[$ind-1].predictions.seconds[0]
    while (!$times[$ind].predictions) {Write-AP ">!Skipping intermediate stop [$($Stops[$ind])]";if (++$ind -ge $times.length) {return "NA"}}
    $times[$ind].predictions.seconds | foreach {if (($_-$src) -ge 60) {return $_-$src}}
    return "WADDA_Fuck"
}
function Gen-DataPoint($stops,$time,$rt) {
    return [PSCustomObject]@{"Source"=$stops[0];"Dest"=$stops[1];"Dur"=$time;"Route"=$rt}
}
foreach ($rt in ($JSON.routes | gm -MemberType NoteProperty).Name) {
    if ($rt -in 's','w1','w2') {Write-AP "!SKIPPING Shuttle Bus [$rt]";continue}
    $Route = Get-Resource $rt
    if (!$Route) {Write-AP "!Bus data for [$rt] unavailable";continue}
    $Stops = $JSON.routes.$rt.stops
    foreach ($i in 0..($Route.length-1)) {
        Write-AP "+Stops: $(Print-List $Stops[($i-1),$i])"
        $DB += Gen-DataPoint $Stops[($i-1),$i] (Diffr $Route $i) $rt
    }
}

$DB | ConvertTo-Json -Compress | Out-File -encoding ascii Edge-Data.ap.json
