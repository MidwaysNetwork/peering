#!/usr/bin/perl -w

use strict;
use XML::Twig;
use POSIX qw(strftime);

if (scalar(@ARGV) lt 2) {
  print STDERR "usage: peers2bgpConfig.pl <xml-source> <ix> <as-number>\n";
  exit -1;
}

my ($xml_source, $target_ix, $target_asn) = @ARGV;

my $sessions = {};

sub regSession {
  my ($t, $peer) = @_;

  my $ix = $peer->{'att'}->{'ix'};
  return unless ($ix eq $target_ix);

  my ($name, $ip, $as, $contact, $max_prefixes, $view, 
      $as_set, $pfx_in, $pfx_out, $map_in, $map_out) = (
	$peer->first_child('name')->text,
	$peer->first_child('ip')->text,
	$peer->first_child('as')->text,
	$peer->first_child('contact'),
	$peer->first_child('max-prefixes'),
	$peer->first_child('view'),
	$peer->first_child('as-set'),
	$peer->first_child('prefix-in'),
	$peer->first_child('prefix-out'),
	$peer->first_child('map-in'),
	$peer->first_child('map-out')
	);

  if (defined $contact) {
    $contact = $contact->text;
  } else {
    $contact = "nomail";
  }

  if (defined $target_asn) {
    if ($target_asn != /^$/) {
      return unless ($target_asn eq $as);
    }
  }

  if ($target_ix =~ /(panap|sfinx)/i) {

    my $pp = $target_ix; 
    $pp =~ tr/a-z/A-Z/;

    printf STDOUT "neighbor %s remote-as %s\n", $ip, $as;
    printf STDOUT "neighbor %s description %s %s\n", $ip, $name, $contact;
    printf STDOUT "neighbor %s shutdown\n", $ip;
    if ($max_prefixes) {
      printf STDOUT "neighbor %s maximum-prefix %s\n", 
	     $ip, $max_prefixes->text;
    }
    printf STDOUT "neighbor %s peer-group %s\n", $ip, $pp;
    if ($pfx_in) {
      printf STDOUT "neighbor %s prefix-list %s in\n", $ip, $pfx_in->text;
    }
    if ($pfx_out) {
      printf STDOUT "neighbor %s prefix-list %s out\n", $ip, $pfx_out->text;
    }
    if ($map_in) {
      printf STDOUT "neighbor %s route-map %s in\n", $ip, $map_in->text;
    }
    if ($map_out) {
      printf STDOUT "neighbor %s route-map %s out\n", $ip, $map_out->text;
    }
    printf STDOUT "no neighbor %s shutdown\n", $ip;
  } else {
    printf STDOUT "neighbor %s remote-as %s\n", $ip, $as;
    printf STDOUT "neighbor %s description %s %s\n", $ip, $name, $contact;
    printf STDOUT "neighbor %s shutdown\n", $ip;
    if ($ip =~ /:/o) {
      printf STDOUT "no neighbor %s activate\n", $ip;
      printf STDOUT "address-family ipv6\n";
      printf STDOUT "neighbor %s maximum-prefix %s\n", 
	     $ip, $max_prefixes ? $max_prefixes->text : 10;
      printf STDOUT "neighbor %s prefix-list %s in\n", 
	     $ip, $pfx_in ? $pfx_in->text : "peer-ip6-in";
      if (defined($pfx_out)) {
	printf STDOUT "neighbor %s prefix-list %s out\n", $ip, $pfx_out->text;
      }
    } else {
      printf STDOUT "neighbor %s maximum-prefix %s\n", 
	     $ip, $max_prefixes ? $max_prefixes->text : 100;
      printf STDOUT "neighbor %s prefix-list %s in\n", 
	     $ip, $pfx_in ? $pfx_in->text : "pfx-all-but-gitoyen";
      printf STDOUT "neighbor %s prefix-list %s out\n", 
	     $ip, $pfx_out ? $pfx_out->text : "pfx-all";
    }
    printf STDOUT "neighbor %s route-map %s in\n", 
	   $ip, $map_in ? $map_in->text : "$ix-in";
    printf STDOUT "neighbor %s route-map %s out\n", 
	   $ip, $map_out ? $map_out->text : "$ix-out";
    printf STDOUT "neighbor %s soft-reconfiguration inbound\n", $ip;
    if ($ip =~ /:/o) {
      printf STDOUT "exit-address-family\n";
    }
    printf STDOUT "no neighbor %s shutdown\n", $ip;
  }
}

my $t = XML::Twig->new( twig_handlers => { 'peer' => \&regSession } );
$t->parsefile($xml_source);

exit 0;

