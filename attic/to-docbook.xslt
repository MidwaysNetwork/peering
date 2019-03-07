<?xml version='1.0'?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version='1.0'>

  <xsl:output method="xml"
    doctype-system="dtd/docbook-xml/docbookx.dtd" 
    doctype-public="-//Norman Walsh//DTD DocBk XML V3.1//EN"
    indent="yes"/>

  <xsl:template match="/">
    <table>
      <title>Gitoyen peers</title>
      <tgroup cols="4">
	<tbody>
	  <xsl:apply-templates/>
	</tbody>
      </tgroup>
    </table>
  </xsl:template>
  
  <xsl:template match="/peers/peer">
    <row>
      <entry><xsl:value-of select="name"/></entry>
      <entry><xsl:value-of select="@ix"/></entry>
      <entry><xsl:value-of select="as"/></entry>
      <entry><xsl:value-of select="contact"/></entry>
      <entry><xsl:value-of select="ip"/></entry>
    </row>
  </xsl:template>

</xsl:stylesheet>

