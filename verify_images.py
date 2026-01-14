#!/usr/bin/env python3
import os

# All IMG numbers processed by the script
img_numbers = [1288, 1289, 1292, 1293, 1294, 1299, 1300, 1301, 1303, 1304, 1305, 1307, 1309, 1310, 1313, 1315, 1316, 1317, 1319, 1320, 1321, 1328, 1329, 1331, 1332, 1334, 1342, 1344, 1346, 1350, 1353, 1361, 1362, 1363, 1369, 1371, 1372, 1375, 1376, 1377, 1380, 1382, 1383, 1385, 1390, 1393, 1397, 1399, 1407, 1408, 1415, 1420, 1446, 1452, 1456, 1459, 1461, 1462, 1463, 1464, 1465, 1469, 1474, 1477, 1481, 1509, 1513, 1515, 1518, 1520, 1527, 1529, 1534, 1538, 1539, 1542, 1543, 1544, 1549, 1550, 1551, 1553, 1554, 1555, 1562, 1565, 1567, 1578, 1579, 1580, 1590, 1594, 1595, 1597, 1598, 1599, 1600, 1601, 1602, 1603, 1623, 1624, 1630, 1633, 1634, 1657, 1662, 1670, 1671, 1673, 1677, 1681, 1691, 1695, 1714, 1715, 1722, 1737, 1740, 1742, 1744, 1746, 1747, 1749, 1752, 1762, 1766, 1776, 1785, 1790, 1792, 1794, 1798, 1809, 1811, 1814, 1816, 1817, 1834, 1835, 1837, 1838, 1839, 1840, 1849, 1852, 1853, 1862, 1881, 1885, 1894, 1895, 1911, 1921, 1927, 1933, 1938, 1939, 1946, 1949, 1950, 1975, 1982, 1984, 1986, 1994, 2019, 2027, 2033, 2034, 2035, 2038, 2039, 2042, 2044, 2048, 2050, 2051, 2053, 2054, 2055]

base_path = '/Users/boots/Sites/birdsofplay-static'
thumbs_path = os.path.join(base_path, 'pics/thumbs')
full_path = os.path.join(base_path, 'pics/full')

missing = []

for num in img_numbers:
    thumb_file = f'img_{num}_320.jpg'
    full_file = f'img_{num}_1600.jpg'
    
    thumb_exists = os.path.exists(os.path.join(thumbs_path, thumb_file))
    full_exists = os.path.exists(os.path.join(full_path, full_file))
    
    if not thumb_exists or not full_exists:
        missing.append({
            'number': num,
            'thumb': thumb_exists,
            'full': full_exists
        })

if missing:
    print(f'Found {len(missing)} images with missing files:')
    for item in missing:
        status = []
        if not item['thumb']:
            status.append('thumbnail missing')
        if not item['full']:
            status.append('full-size missing')
        print(f"  IMG_{item['number']}: {', '.join(status)}")
    
    # Create missing-images.txt
    with open(os.path.join(base_path, 'missing-images.txt'), 'w') as f:
        f.write('Missing Image Files Report\n')
        f.write('='*50 + '\n\n')
        for item in missing:
            f.write(f"IMG_{item['number']}:\n")
            if not item['thumb']:
                f.write(f"  - Thumbnail: pics/thumbs/img_{item['number']}_320.jpg (MISSING)\n")
            if not item['full']:
                f.write(f"  - Full-size: pics/full/img_{item['number']}_1600.jpg (MISSING)\n")
            f.write('\n')
    print(f'\nMissing images log created: missing-images.txt')
else:
    print('✓ All 181 referenced image files exist in both thumbs and full folders!')
    print('  - 181 thumbnail files verified')
    print('  - 181 full-size files verified')
