select count(*), recipientCount, formalityLabel from
(
	select count(*) as recipientCount, formality.EffectiveLabel as formalityLabel from message 
	INNER JOIN recipientinfo
	on message.mid = recipientinfo.mid
	INNER JOIN formality
	on message.mid = formality.mid
	where formality.EffectiveLabel = 1
		and message.sender like '%@enron.com%'
	GROUP BY message.mid 
	ORDER BY recipientCount
) temp 
GROUP BY recipientCount, formalityLabel
