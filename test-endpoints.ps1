# test-endpoints.ps1

$baseUrl = "http://localhost:8000"

function Format-Response {
    param (
        [PSCustomObject]$Response
    )
    $Response | ConvertTo-Json -Depth 10
}

function Invoke-APIRequest {
    param (
        [string]$Method,
        [string]$Endpoint,
        [object]$Body,
        [string]$Token
    )
    
    $headers = @{
        "Content-Type" = "application/json"
    }
    
    if ($Token) {
        $headers["Authorization"] = "Bearer $Token"
    }
    
    $params = @{
        Method = $Method
        Uri = "$baseUrl$Endpoint"
        Headers = $headers
    }
    
    if ($Body) {
        $params["Body"] = ($Body | ConvertTo-Json)
    }
    
    try {
        $response = Invoke-RestMethod @params
        Write-Host "$Method $Endpoint - Success" -ForegroundColor Green
        Write-Host "Response:" -ForegroundColor Yellow
        Write-Host (Format-Response $response) -ForegroundColor Gray
        return $response
    }
    catch {
        Write-Host "$Method $Endpoint - Failed: $($_.Exception.Response.StatusCode)" -ForegroundColor Red
        try {
            $reader = New-Object System.IO.StreamReader($_.Exception.Response.GetResponseStream())
            $reader.BaseStream.Position = 0
            $reader.DiscardBufferedData()
            $errorResponse = $reader.ReadToEnd()
            Write-Host "Error Details:" -ForegroundColor Yellow
            Write-Host $errorResponse -ForegroundColor Gray
        }
        catch {
            Write-Host "No detailed error message available" -ForegroundColor Yellow
        }
        return $null
    }
}

Write-Host "Starting API endpoint tests..." -ForegroundColor Cyan

# Test 1: API Root
Write-Host "`nTesting API Root" -ForegroundColor Yellow
$rootResponse = Invoke-APIRequest -Method "GET" -Endpoint "/"

# Test 2: User Registration
Write-Host "`nTesting User Registration" -ForegroundColor Yellow
$registerBody = @{
    username = "testuser$(Get-Random)"
    email = "testuser$(Get-Random)@example.com"
    password = "TestPass123!"
}
$registerResponse = Invoke-APIRequest -Method "POST" -Endpoint "/api/users/register/" -Body $registerBody

if ($registerResponse) {
    $token = $registerResponse.access
    
    # Test 3: Products List
    Write-Host "`nTesting Products List" -ForegroundColor Yellow
    $productsResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/products/" -Token $token
    
    # Test 4: Shops List
    Write-Host "`nTesting Shops List" -ForegroundColor Yellow
    $shopsResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/shops/" -Token $token
    
    # Test 5: Orders List
    Write-Host "`nTesting Orders List" -ForegroundColor Yellow
    $ordersResponse = Invoke-APIRequest -Method "GET" -Endpoint "/api/orders/" -Token $token
}

Write-Host "`nAPI endpoint tests completed" -ForegroundColor Cyan