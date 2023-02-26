import discord


class MariageConfirmationView(discord.ui.View):
    def __init__(self, target: discord.Member):
        super().__init__()
        self.timeout = None
        self.marriage_accepted: bool | None = None
        self.target = target

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green, row=1)
    async def accept(self, _: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.target:
            print(interaction.user, self.target)
            await interaction.response.send_message(
                "ur not the one getting married, silly :3"
            )
            return

        user_who_replied = interaction.user
        mention = user_who_replied.mention \
            if user_who_replied is not None else "<something went wrong :‹>"
        await interaction.response.send_message(
            f"{mention} accepted the proposal :3 lovely"
        )

        self.marriage_accepted = True
        self.stop()

    @discord.ui.button(label="Deny", style=discord.ButtonStyle.red, row=1)
    async def deny(self, _: discord.ui.Button, interaction: discord.Interaction):
        if interaction.user != self.target:
            await interaction.response.send_message(
                "ur not the one getting married, silly :3"
            )
            return

        user_who_replied = interaction.user
        mention = user_who_replied.mention \
            if user_who_replied is not None else "<something went wrong :‹>"

        await interaction.response.send_message(
            f"{mention} didn't wanna get married yet..."
        )

        self.marriage_accepted = False
        self.stop()
