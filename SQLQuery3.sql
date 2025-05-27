SELECT ContentID,
	   CampaignID,
	   ProductID,
	   --LOWER(ContentType) AS ContentType,
	   REPLACE(ContentType , 'socialmedia' , 'Social Media') AS ContentType,
	   likes,
	   LEFT(ViewsClicksCombined, CHARINDEX('-', ViewsClicksCombined) - 1) AS Views, 
       RIGHT(ViewsClicksCombined, LEN(ViewsClicksCombined) - CHARINDEX('-', ViewsClicksCombined)) AS Clicks,
	   FORMAT(CONVERT(DATE , EngagementDate) , 'dd.MM.yyyy') AS EngagementDate

FROM dbo.engagement_data;

