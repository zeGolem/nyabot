import discord


class ConfirmationView(discord.ui.View):
    def __init__(self, timeout: float | None):
        super().__init__()
        self.timeout = timeout
        self.user_accepted: bool | None = None

    def _user_can_respond(self, user: discord.User | discord.Member):
        pass

    async def __on_wrong_user(self, interaction: discord.Interaction):
        pass

    async def _on_accept(self, interaction: discord.Interaction, replyer: discord.User | discord.Member):
        pass

    async def _on_deny(self, interaction: discord.Interaction, replyer: discord.User | discord.Member):
        pass

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, row=1)
    async def accept(self, _: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user is None:
            await interaction.response.send_message("something went wrong :(")
            return
        if not self._user_can_respond(interaction.user):
            await self.__on_wrong_user(interaction)
            return

        await self._on_accept(interaction, interaction.user)

        self.user_accepted = True
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, row=1)
    async def deny(self, _: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user is None:
            await interaction.response.send_message("something went wrong :(")
            return
        if not self._user_can_respond(interaction.user):
            await self.__on_wrong_user(interaction)
            return

        await self._on_deny(interaction, interaction.user)

        self.user_accepted = False
        self.stop()


class MariageConfirmationView(ConfirmationView):
    def __init__(self, target: discord.Member):
        super().__init__(timeout=15*60)  # 15 minues timeout
        self.target = target

    def _user_can_respond(self, user: discord.User | discord.Member):
        return user == self.target

    async def _on_wrong_user(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "ur not the one getting married, silly :3", ephemeral=True, delete_after=10
        )

    async def _on_accept(self, interaction: discord.Interaction, replyer: discord.User | discord.Member):
        await interaction.response.send_message(
            f"{replyer.mention} accepted the proposal :3 so cute!"
        )

    async def _on_deny(self, interaction: discord.Interaction, replyer: discord.User | discord.Member):
        await interaction.response.send_message(
            f"{replyer.mention} isn't ready yet..."
        )


class PolyculeMemberJoinConfirmationView(ConfirmationView):
    def __init__(self, target: discord.User):
        super().__init__(timeout=15*60)
        self.target = target

    def _user_can_respond(self, user: discord.User | discord.Member):
        return user == self.target

    async def _on_wrong_user(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            "ur not the one getting married, silly :3", ephemeral=True, delete_after=10
        )

    async def _on_accept(self, interaction: discord.Interaction, replyer: discord.User | discord.Member):
        await interaction.response.send_message(
            f"{replyer.mention} is okay for extending the polycule :3 kawaii desune~"
        )

    async def _on_deny(self, interaction: discord.Interaction, replyer: discord.User | discord.Member):
        await interaction.response.send_message(
            f"{replyer.mention} isn't ready yet..."
        )
