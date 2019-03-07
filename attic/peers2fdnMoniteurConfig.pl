#!/usr/bin/perl -w

use strict;
use XML::Twig;
use POSIX qw(strftime);

exit -1 unless (scalar(@ARGV) eq 1);
my ($filename) = @ARGV;

my $sessions = {};

sub regSession {
  my ($t, $peer) = @_;
  my $name = $peer->first_child('name');
  
  $sessions->{$name->text} = []
    unless exists $sessions->{$name->text};
  
  push @{ $sessions->{$name->text} }, {
    'pop' => $peer->{'att'}->{'ix'},
    'ip' => $peer->first_child('ip')
  };
}

my $t = XML::Twig->new( twig_handlers => { 'peer' => \&regSession } );
$t->parsefile($filename);

print STDOUT "{\n";
foreach my $peer (keys %{ $sessions }) {
  my @ps = @{ $sessions->{$peer} };
   
  print STDOUT "  '$peer' => {\n"; 
  if (scalar(@ps) eq 1) {
    print STDOUT "    'sort' => 'single',\n"; 
  } else {
    print STDOUT "    'sort' => 'any',\n"; 
  }
  print STDOUT "    'sessions' => {\n"; 
  foreach my $pi (@ps) {
    if ($pi->{'ip'}->text !~ /:/) {
      print STDOUT "      '".$pi->{'pop'}."' => "; 
      print STDOUT "'".$pi->{'ip'}->text."',\n"; 
    }
  }
  print STDOUT "    },\n";
  print STDOUT "  },\n";
}
print STDOUT "}\n";

exit 0;

