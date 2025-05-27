SELECT *
FROM customer_reviews;


SELECT ReviewID,
	   CustomerID,
	   ProductID,
	   ReviewDate,
	   Rating,
	   REPLACE(ReviewText , '  ',' ') AS ReviewText
	

FROM customer_reviews