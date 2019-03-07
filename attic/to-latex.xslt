<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version='1.0'>

  <xsl:output method="text"/>

  <xsl:strip-space elements="*"/>

  <xsl:template match="/">
\documentclass[a4paper,11pt]{article}
\setlength{\oddsidemargin}{0cm}
\setlength{\evensidemargin}{0cm}
\setlength{\topmargin}{0cm}
\setlength{\headheight}{0cm}
\setlength{\headsep}{0cm}
\usepackage{url}
\usepackage{supertabular}
\usepackage{palatino}
\title{Gitoyen peers}
\author{Stephane Bortzmeyer, \url{bortzmeyer@gitoyen.net}}
\begin{document}
\sloppy
\maketitle

\center{\textbf{Generated by the XSL tool <xsl:value-of
      select="system-property('xsl:vendor')"/> (\url{<xsl:value-of
      select="system-property('xsl:vendor-url')"/>})}}


\begin{supertabular}{|p{4.5cm}|l|c|p{5.25cm}|c|}
\hline
\textbf{Name}&amp;\textbf{IXP}&amp;\textbf{AS}&amp;\textbf{Contact}&amp;\textbf{IP address}\\
\hline\hline
    <xsl:apply-templates/>
    \end{supertabular}
    \end{document}
  </xsl:template>
  
  <xsl:template match="/peers/peer">
    <xsl:value-of select="name"/>
&amp;
    <xsl:value-of select="@ix"/>
&amp;
    <xsl:value-of select="as"/>
&amp;
\url{<xsl:value-of select="contact"/>}
&amp;
    <xsl:value-of select="ip"/>
\\
\hline
  </xsl:template>

</xsl:stylesheet>

