SELECT * 
FROM dbo.customers;

SELECT CustomerID,
	   CustomerName,
	   Email,
	   Gender,
	   Age,
	   Country,
	   City

FROM dbo.customers
LEFT JOIN dbo.geography
ON dbo.customers.GeographyID = dbo.geography.GeographyID