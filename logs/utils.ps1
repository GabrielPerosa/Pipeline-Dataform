function Get-GoogleCloudLogs {
    param (
        [Parameter(Mandatory = $true)]
        [string]$ProjectId,

        [Parameter(Mandatory = $false)]
        [int]$Limit = 5,

        [Parameter(Mandatory = $false)]
        [string]$Filter = 'protoPayload.methodName="jobservice.getqueryresults"'
    )

    Write-Output "Lendo logs do projeto '$ProjectId' com filtro '$Filter'..."
    $logs = gcloud logging read $Filter --limit=$Limit --format=json --project=$ProjectId | ConvertFrom-Json

    $logs | ForEach-Object {
        Write-Output "Log encontrado:"

        if ($_.protoPayload -and $_.protoPayload.serviceData -and $_.protoPayload.serviceData.jobGetQueryResultsResponse -and $_.protoPayload.serviceData.jobGetQueryResultsResponse.job -and $_.protoPayload.serviceData.jobGetQueryResultsResponse.job.jobStatistics) {
            $jobStatistics = $_.protoPayload.serviceData.jobGetQueryResultsResponse.job.jobStatistics

            $totalBilledBytes = $jobStatistics.totalBilledBytes
            $totalProcessedBytes = $jobStatistics.totalProcessedBytes

            Write-Output "`n- Valores extraídos:"
            Write-Output "  Total Billed Bytes: $totalBilledBytes"
            Write-Output "  Total Processed Bytes: $totalProcessedBytes"
        } else {
            Write-Warning "- Propriedade 'jobStatistics' ou suas propriedades não encontradas."
        }

        Write-Output ("-" * 50)
    }
}