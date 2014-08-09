select positions.Position,
	positions.rank as Rank, 
	count(*) as Total_Emails, 
	sum(formality.EffectiveLabel=1) as Formal, 
	sum(formality.EffectiveLabel=2) as Informal,
	sum(formality.EffectiveLabel=2)/count(*) as Informal_Percent,
	sum(requests.RawLabel=0) as NonRequests,
	sum(requests.RawLabel=1) as Requests,
	sum(requests.RawLabel=1)/count(*) as Request_Percent from message
INNER JOIN formality
on message.mid = formality.mid
INNER JOIN requests
on message.mid = requests.mid
INNER JOIN positions
on message.sender = positions.Address
GROUP BY positions.Position
ORDER BY positions.rank DESC