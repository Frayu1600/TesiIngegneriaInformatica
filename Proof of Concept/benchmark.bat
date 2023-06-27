@echo off
setlocal enabledelayedexpansion

set curves=P-192 P-224 P-256 P-384 P-521

for %%i in (%curves%) do (
  echo Testing curve %%i
  echo. > "%%i benchmark tests.txt"

  for /L %%j in (1, 1, 20) do (
    echo Iteration number %%j...

    python "EC_DRBG_vuln.py" %%i >> "%%i benchmark tests.txt"

    echo iteration number %%j complete
  )
  echo tests for curve %%i complete
)

echo all tests complete!

pause
endlocal