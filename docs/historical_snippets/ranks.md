https://gist.github.com/LatvianModder/54ccaee3af7a55d23831eac20f248a3f/0ba8846e95ba1b9f4057b81cae74de96dc262f15


power determines the rank hierarchy, if multiple permissions are applied for the same player and two permissions conflict, the rank permission with the highest 
power will be the one applied.
condition determines when the rank is applied, if there is no condition specified it can only be applied manually with /ftbranks add <player> <rank>
always_active is a condition that means the rank is always applied, it is generally used for default ranks that would typically have the lowest priority/power.
op condition applies when a player has been opped (with /op) or on singleplayer with cheats enabled.

Some other conditions available are dimension, location, spawn, ftbchunks:claimed_chunk. Logical comparators like not, and, or and xor can be used to combine mu
ltiple conditions. Lastly the playtime condition can be used with time and time_unit properties to auto-promote ranks after a specified time has passed. Valid t
ime units are ticks, seconds, minutes, hours, days and weeks.

