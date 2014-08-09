select count(*), formality.EffectiveLabel as formalityValue, requests.RawLabel as requestValue from message
INNER JOIN formality 
on message.mid = formality.mid
INNER JOIN requests
on requests.mid = message.mid
WHERE formality.LineCount > 0
GROUP BY requests.RawLabel, formality.EffectiveLabel
