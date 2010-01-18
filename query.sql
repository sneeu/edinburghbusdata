SELECT s.sms, s.name, v.mnemonic FROM busstop s
LEFT JOIN stop ON s.sms = stop.busstop
LEFT JOIN service v ON stop.service = v.mnemonic
WHERE s.sms = '36232323';