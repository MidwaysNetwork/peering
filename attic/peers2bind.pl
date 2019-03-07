#!/usr/bin/perl -w

use strict;
use XML::Twig;
use POSIX qw(strftime);

exit -1 unless (scalar(@ARGV) eq 2);

#my $version = strftime "%Y%m%d%H", gmtime();
my $version = strftime "%s", gmtime();

print "
\$TTL 7200

@	IN      SOA     ns.gitoyen.net. hostmaster.gitoyen.net. ( $version 21600 3600 3600000 259200 )
  IN  NS  ns.gitoyen.net.
  IN  NS  ns2.gitoyen.net.
@	IN      MX      10 mail.gitoyen.net.

";

my ($filename, $pop) = @ARGV;

sub writeArecord {
  my ($t, $peer) = @_;

  if ($peer->{'att'}->{'ix'} =~ /$pop/) {
    my $ip = $peer->first_child('ip');
    my $name = $peer->first_child('name');
    my $as = $peer->first_child('as');
    my $contact = $peer->first_child('contact');
  
    if ($ip->text =~ /:/o) {
      print "AS" . $as->text . "\tIN AAAA ". $ip->text . "\n";
    } else {
      print "AS" . $as->text . "\tIN A ". $ip->text . "\n";
    }
    print "\tIN TXT " . $contact->text . "\n" if defined $contact;
    print "\tIN HINFO \"" . $name->text . "\" \"$pop\"\n" if defined $name;
  }
}

my $t = XML::Twig->new( twig_handlers => { 'peer' => \&writeArecord } );
$t->parsefile($filename);

