# scry Homebrew formula.
#
# This is a reference copy. The canonical location is your tap repo
# (github.com/ankurkotwal/homebrew-scry) at Formula/scry.rb.
#
# Release process:
#   1. Tag the scry source repo:
#        git tag v0.1.0 && git push origin v0.1.0
#   2. Compute the tarball sha256:
#        curl -sL https://github.com/ankurkotwal/scry/archive/refs/tags/v0.1.0.tar.gz | sha256sum
#   3. Update `url` and `sha256` below, copy this file into the tap repo,
#      commit, and push.
#
# Users install with:
#   brew install ankurkotwal/scry/scry

class Scry < Formula
  desc "One-line system status dashboard, byobu-inspired"
  homepage "https://github.com/ankurkotwal/scry"
  url "https://github.com/ankurkotwal/scry/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "e10b01305aea0a7de2d535bbc2e580dee8bf03cf8791d9d0d6b62f28585e28a5"
  license "Apache-2.0"

  livecheck do
    url :stable
    strategy :github_latest
  end

  def install
    bin.install "scry"
  end

  test do
    assert_match(/^Usage: scry/, shell_output("#{bin}/scry --help"))
  end
end
