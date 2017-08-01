import sbt._

object MyBuild extends Build {

  lazy val soundPlayerProject = RootProject(uri("git://github.com/alvinj/SoundFilePlayer.git"))

}
