import Dependencies._

lazy val root = (project in file(".")).
  settings(
    inThisBuild(List(
      organization := "com.lucyearth",
      scalaVersion := "2.12.2",
      version      := "0.1"
    )),
    name := "LEDServer",
    libraryDependencies += scalaTest % Test,
    libraryDependencies += "com.fazecast" % "jSerialComm" % "[1.0.0,2.0.0)"
  )
