use strict;
use warnings;
my $feelevels = 46;

print <<"EOF";
CREATE TABLE IF NOT EXISTS mempool (
    time INTEGER NOT NULL PRIMARY KEY,
EOF

for my $i (0..($feelevels - 1)) {
    print "    cnt$i INTEGER,\n";
}
for my $i (0..($feelevels - 1)) {
    print "    size$i INTEGER,\n";
}
for my $i (0..($feelevels - 1)) {
    my $comma = $i < $feelevels - 1 ? "," : "";
    print "    fee$i INTEGER$comma\n";
}
print ");\n";
