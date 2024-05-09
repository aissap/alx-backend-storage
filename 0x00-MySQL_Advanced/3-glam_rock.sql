-- List all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name,
       IF NULL(SPLIT_STR(lifespan, '-', 1), 2022) - IFNULL(SPLIT_STR(lifespan, '-', 2), 2022) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;