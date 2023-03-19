As part of the clean-up process for the project, the project moving to a new development strategy based on the "[OneFlow](https://www.endoflineblog.com/oneflow-a-git-branching-model-and-workflow)" methodology. As a result, I have created a "dev" branch which will now contain ongoing prerelease code base changes. This means that all PRs moving forward should be based on the "dev" branch and not the "master" branch.

Following the next stable production release of version 0.4.0, the "master" branch will become tied to the current production release version. Accordingly, the "latest" tag of the project's Docker image (powerdnsadmin/pda-legacy) will continue to follow the "master" branch of the repository. This means that following the next production release of version 0.4.0, the "latest" Docker image tag will begin representing the latest production release.

Additionally, the new "dev" branch of the repository has been setup to provide automatic Docker image builds under the "dev" tag of the official project Docker image powerdnsadmin/pda-legacy.

Thank you all for participating in the community and/or being a loyal PDA user!