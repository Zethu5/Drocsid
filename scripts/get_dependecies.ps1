function genReqtxt {
    try {
        
        pip install pipreqs
        pipreqs . 
    }
    catch {
        Write-Host "Couldn't generate requirements.txt"
    }
    
}

function installDep {
   try {
        pip install -r requirements.txt
   }
   catch {
    Write-Host "Couldn't install dependencies"
   }
}

Get-Date
Write-host "Dependencies installation starting `r`nPlease verify you have Pip installed"
Set-Location ..\src
genReqtxt
installDep
