select count(*), formality_label, rankDiff from 
(
	select message.mid, count(*) as recipientCount, formality.EffectiveLabel as formality_label,
		(recipientPosition.Rank - senderPosition.rank) as rankDiff from message
	INNER JOIN recipientinfo
	on message.mid = recipientinfo.mid
	INNER JOIN formality
	on message.mid = formality.mid
	INNER JOIN positions senderPosition
	on message.sender = senderPosition.Address
	INNER JOIN positions recipientPosition
	on recipientinfo.rvalue = recipientPosition.Address
    where senderPosition.Rank != 0 and recipientPosition.Rank != 0
	GROUP BY message.mid
) temp
where recipientCount = 1
GROUP BY rankDiff, formality_label